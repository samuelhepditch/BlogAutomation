import React, { useState } from "react";
import { RequestStatus } from "../data/RequestStatus";
import { BlogService } from "../backend/BlogService";
import Blog from "../data/Blog";
import { BlogState } from "../data/BlogState";
import StatusDropDown from "./StatusDropdown";

type InputFormProps = {
  blogs: Array<Blog>;
  addBlog: (
    blogIndex: number,
    blogTitle: string,
    blogKeywords: string,
    blogState: BlogState
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
  const [blogState, setBlogState] = useState<BlogState>(BlogState.draft);

  const blogService = new BlogService(true);

  const handleSubmit = async (event: React.SyntheticEvent) => {
    event.preventDefault();
    const blogIndex = props.blogs.length;

    props.addBlog(blogIndex, blogTitle, blogKeyWords, blogState);
    try {
      const response = await blogService.writeBlog(
        blogTitle,
        blogKeyWords,
        blogState
      );
      console.log(response.data.status);
      if (response.data.status === "error") {
        props.updateBlogStatus(blogIndex, RequestStatus.failed);
      } else {
        props.updateBlogStatus(blogIndex, RequestStatus.success);
      }
      props.udpateBlogNotes(blogIndex, response.data.message);
    } catch (e: unknown) {
      props.updateBlogStatus(blogIndex, RequestStatus.failed);
      if (e instanceof Error) {
        props.udpateBlogNotes(blogIndex, e.message);
        props.setMessage(`Things exploded (${e.message})`);
      } else {
        props.setMessage(
          "An unknown exception occured when sending a request."
        );
      }
      props.showAlertHandler();
    }
  };

  return (
    <div className="col-md-6 offset-md-3">
      <h3>Create a Blog Post</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
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
            required
          />
        </div>
        <div className="mb-3">
          <StatusDropDown updateBlogState={setBlogState} />
        </div>

        <button type="submit" className="btn btn-primary">
          Write Blog Post
        </button>
      </form>
    </div>
  );
};

export default BlogForm;
