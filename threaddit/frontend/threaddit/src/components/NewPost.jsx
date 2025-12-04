import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import Markdown from "markdown-to-jsx";
import PropTypes from "prop-types";
import { useState } from "react";
import avatar from "../assets/avatar.png";
import AuthConsumer from "./AuthContext";
import Loader from "./Loader";
import { ThreadSearch } from "./Navbar";
import Svg from "./Svg";

NewPost.propTypes = {
  setShowModal: PropTypes.func,
  isEdit: PropTypes.bool,
  postInfo: PropTypes.object,
  threadInfo: PropTypes.object,
};

export default function NewPost({ setShowModal, isEdit = false, postInfo = {}, threadInfo = {} }) {
  const queryClient = useQueryClient();
  const [title, setTitle] = useState(postInfo?.title || "");
  const [content, setContent] = useState(postInfo?.content || "");
  const [media, setMedia] = useState(null);
  const [preMd, setPreMd] = useState(false);
  const [mediaType, setMediaType] = useState("media"); // "media" | "url"
  const [imageUrl, setImageUrl] = useState("");
  // Accept either { id, name } or { thread_id, thread_name }
  const [thread, setThread] = useState(
    isEdit
      ? { id: threadInfo.thread_id, name: threadInfo.thread_name }
      : false
  );

  const { user } = AuthConsumer();

  const { mutate: handleSubmit, status } = useMutation({
    mutationFn: async (e) => {
      e?.preventDefault();

      // ---- client-side guards to avoid 400s ----
      const trimmedTitle = (title || "").trim();
      if (!trimmedTitle) {
        alert("Please enter a title");
        return;
      }
      const subthreadId = thread?.id ?? thread?.thread_id;
      if (!subthreadId) {
        alert("Please select a community/thread first");
        return;
      }

      // ---- Build FormData EXACTLY as backend expects ----
      const formData = new FormData();
      formData.append("title", trimmedTitle);
      // repo’s post endpoint expects these keys:
      // content_type: "media" | "url"
      // content_url: string (if mediaType === "url")
      // content: the text body
      formData.append("content_type", mediaType);
      formData.append("content_url", imageUrl || "");
      formData.append("content", content || "");
      if (media) {
        formData.append("media", media, media.name);
      }
      formData.append("subthread_id", subthreadId);

      for (const [k, v] of formData.entries()) console.log("POST formData:", k, v);


      if (!isEdit) {
        await axios
          .post("/api/post", formData, { headers: { "Content-Type": "multipart/form-data" } })
          .then(() => {
            setShowModal(false);
            // Optionally refresh lists
            queryClient.invalidateQueries({ queryKey: ["posts"] });
          })
          .catch((err) => alert(`${err.message} check your fields, Title is mandatory`));
      } else {
        await axios
          .patch(`/api/post/${postInfo.id}`, formData, { headers: { "Content-Type": "multipart/form-data" } })
          .then((res) => {
            queryClient.setQueryData(["post/comment", `${postInfo.id}`], (oldData) => {
              return { ...oldData, post_info: res.data.new_data };
            });
            setShowModal(false);
          })
          .catch((err) => alert(`${err.message} check your fields, Title and thread is mandatory`));
      }
    },
  });

  return (
    <div className="flex flex-col w-5/6 p-5 space-y-5 rounded-md h-4/6 blur-none md:w-3/4 md:h-5/6 md:p-10 bg-theme-cultured">
      <div className="flex flex-col items-center justify-between p-4 space-y-3 bg-white rounded-xl md:flex-row md:space-y-0">
        <div className="flex items-center space-x-3">
          <p>{isEdit ? "Editing" : "Posting"} as</p>
          <img src={user.avatar || avatar} className="object-cover w-8 h-8 rounded-full md:w-12 md:h-12" alt="" />
          <p>{user.username}</p>
        </div>
        {status === "loading" && <Loader forPosts={true} />}
        <div className="flex items-center mr-2 space-x-2 md:space-x-3">
          <p className="hidden md:block">{isEdit ? "Editing" : "Posting"} on</p>
          <p className="md:hidden">On</p>
          {thread ? (
            <div className="flex items-center p-1 space-x-3">
              {/* show name whether it’s `name` or `thread_name` */}
              <p className="tracking-wide medium text- md:text-base text-theme-orange">
                {thread.name ?? thread.thread_name}
              </p>
              <Svg type="delete" className="w-7 h-7 text-theme-orange" onClick={() => setThread(false)} />
            </div>
          ) : (
            <ThreadSearch callBackFunc={setThread} forPost={true} />
          )}
        </div>
      </div>

      <form
        encType="multipart/form-data"
        onSubmit={handleSubmit}
        className="flex flex-col flex-1 justify-around p-1.5 w-full h-1/2 bg-white rounded-md"
      >
        <label htmlFor="title">
          <span>Title</span>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            type="text"
            name="title"
            id="title"
            className="w-full border-b border-gray-800 focus:outline-none"
            required
          />
        </label>

        <label htmlFor="content">
          <span>{preMd ? "Markdown Preview" : "Content"}</span>
          <button
            type="button"
            className="active:scale-90 ml-5 my-0.5 py-0.5 px-2 bg-blue-600 text-white font-semibold rounded-md"
            onClick={() => setPreMd(!preMd)}
          >
            {preMd ? "close preview" : "preview markdown"}
          </button>

          <div className="flex flex-col space-y-2">
            {preMd ? (
              <div className="max-w-full p-2 overflow-auto prose border border-gray-800 h-28">
                <Markdown options={{ forceBlock: true, wrapper: "div" }} className="w-full">
                  {content.replace("\n", "<br />\n") || "This is markdown preview"}
                </Markdown>
              </div>
            ) : (
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                name="content"
                id="content"
                className="w-full p-2 border border-gray-800 h-28 md:max-h-32 focus:outline-none"
              />
            )}
          </div>
        </label>

        <label htmlFor="media" className="flex flex-col items-center space-y-3 md:space-y-0 md:space-x-5 md:flex-row">
          <select
            className="px-10 py-2 bg-white border rounded-md md:px-12"
            name="mediaType"
            id="mediaType"
            value={mediaType}
            onChange={(e) => setMediaType(e.target.value)}
          >
            <option value="media">Media</option>
            <option value="url">URL</option>
          </select>

          {mediaType === "media" ? (
            <label htmlFor="media">
              <input
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (!f) return;
                  if (f.size > 10 * 1024 * 1024) {
                    alert("File too large, only upload files less than 10MB");
                  } else {
                    setMedia(f);
                  }
                }}
                type="file"
                name="media"
                alt="media"
                accept="image/*, video/*"
                id="media"
                className="w-full focus:outline-none"
              />
            </label>
          ) : (
            <input
              type="text"
              name="media_url"
              id="media_url"
              className="w-full p-2 border border-gray-800 rounded-md focus:outline-none"
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
              placeholder="https://example.com/image-or-video"
            />
          )}
        </label>

        {isEdit && (
          <span className="text-sm font-semibold text-red-500">
            Only Add Image if you want to modify the original image; if empty the original will be used.
          </span>
        )}

        <button
          type="submit"
          disabled={status === "loading"}
          className="py-2 font-semibold text-white rounded-md bg-theme-orange active:scale-95"
        >
          {status === "loading" ? "Submitting..." : "Submit"}
        </button>
      </form>
    </div>
  );
}
