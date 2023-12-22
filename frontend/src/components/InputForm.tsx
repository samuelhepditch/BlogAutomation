import React, { useState } from "react";
import { RequestStatus } from "../data/RequestStatus";
import Blog from "../data/Blog";
import { BlogStatus } from "../data/BlogStatus";
import StatusDropDown from "./StatusDropdown";

type InputFormProps = {
  blogQueue: Array<Blog>;
  addBlogToQueue: (
    blogTitle: string,
    blogKeywords: string,
    blogStatus: BlogStatus
  ) => void;
  updateBlogStatus: (blogIndex: number, status: RequestStatus) => void;
  udpateBlogNotes: (blogIndex: number, message: string) => void;
  showAlertHandler: () => void;
  hideAlertHandler: () => void;
  setMessage: (message: string) => void;
};

const BlogForm: React.FC<InputFormProps> = (props) => {
  const [blogTitle, setBlogTitle] = useState<string>("");
  const [blogKeyWords, setBlogKeywords] = useState<string>("");
  const [blogStatus, setBlogStatus] = useState<BlogStatus>(BlogStatus.draft);

  const wordCount = blogTitle.trim().split(/\s+/).filter(Boolean).length;
  const isWordCountValid = wordCount >= 5 && wordCount <= 12;

  const handleSubmit = async (event: React.SyntheticEvent) => {
    event.preventDefault();
    props.addBlogToQueue(blogTitle, blogKeyWords, blogStatus);
  };

  const inputStatusStyle = {
    color: isWordCountValid ? "green" : "red",
  };

  return (
    <div className="col-md-6 offset-md-3">
      <h3>Create a Blog Post</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <span style={inputStatusStyle}>
            {isWordCountValid
              ? "Word count is within range (5-12)."
              : "Word count is NOT within range (5-12)."}
          </span>
          <br />
          <label htmlFor="blog_title" className="form-label">
            Title
          </label>

          <input
            type="text"
            className="form-control"
            id="blog_title"
            value={blogTitle}
            onChange={(e) => setBlogTitle(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="keywords" className="form-label">
            Keywords (comma-separated)
          </label>
          <input
            type="text"
            className="form-control"
            id="keywords"
            value={blogKeyWords}
            onChange={(e) => setBlogKeywords(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <StatusDropDown updateBlogStatus={setBlogStatus} />
        </div>

        <button type="submit" className="btn btn-primary">
          Write Blog Post
        </button>
      </form>
    </div>
  );
};

export default BlogForm;
