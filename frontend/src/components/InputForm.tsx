import React, { useState } from "react";
import { BlogStatus } from "../data/BlogStatus";
import { BlogService } from "../backend/BlogService";
import Blog from "../data/Blog";

type InputFormProps = {
  blogs: Array<Blog>;
  addBlog: (blogIndex: number) => void;
  updateBlogStatus: (blogIndex: number, status: BlogStatus) => void;
  udpateBlogNotes: (blogIndex: number, message: string) => void;
  showAlertHandler: () => void;
  hideAlertHandler: () => void;
};

const BlogForm: React.FC<InputFormProps> = (props) => {
  const [blogTitle, setBlogTitle] = useState<string>("");
  const [keywords, setKeywords] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const blogService = new BlogService(true);

  const handleSubmit = async (event: React.SyntheticEvent) => {
    event.preventDefault();
    const blogIndex = props.blogs.length;

    props.addBlog(blogIndex);
    try {
      const response = await blogService.writeBlog(blogTitle, keywords);
      console.log(response.data.status);
      if (response.data.status === "error") {
        props.updateBlogStatus(blogIndex, BlogStatus.failed);
      } else {
        props.updateBlogStatus(blogIndex, BlogStatus.success);
      }
      props.udpateBlogNotes(blogIndex, response.data.message);
    } catch (e: unknown) {
      props.updateBlogStatus(blogIndex, BlogStatus.failed);
      if (e instanceof Error) {
        props.udpateBlogNotes(blogIndex, e.message);
        setMessage(`Things exploded (${e.message})`);
      } else {
        setMessage("An unknown exception occured when sending a request.");
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
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Write Blog Post
        </button>
      </form>
    </div>
  );
};

export default BlogForm;
