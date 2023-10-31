import React from "react";
import { useState } from "react";
import axios from "axios";
import BlogTable from "./components/BlogTable";
import Blog from "./data/Blog";
import "bootstrap/dist/css/bootstrap.min.css";
import { BlogService } from "./backend/BlogService";
import { BlogStatus } from "./data/BlogStatus";

function App() {
  const [topic, setTopic] = useState<string>("");
  const [keywords, setKeywords] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [messageType, setMessageType] = useState<string>("");
  const [blogs, setBlogs] = useState<Array<Blog>>([]);

  const blogService = new BlogService(true);

  const addBlog = (blogIndex: number) => {
    let newBlog: Blog = new Blog(
      blogIndex,
      topic,
      keywords,
      BlogStatus.in_progress
    );

    setBlogs((prevBlogs) => [...prevBlogs, newBlog]);
  };

  const updateBlogStatus = (blogIndex: number, status: BlogStatus) => {
    setBlogs((prevBlogs) => {
      const updatedBlogs = [...prevBlogs];
      updatedBlogs[blogIndex].status = status;
      return updatedBlogs;
    });
  };

  const handleSubmit = async (event: React.SyntheticEvent) => {
    event.preventDefault();
    const blogIndex = blogs.length;

    addBlog(blogIndex);
    try {
      const response = await blogService.writeBlog(topic, keywords);

      setMessage(response.data.message);
      setMessageType("success");

      updateBlogStatus(blogIndex, BlogStatus.success);
    } catch (e: unknown) {
      setMessageType("error");
      updateBlogStatus(blogIndex, BlogStatus.failed);
      if (e instanceof Error) {
        return {
          message: `Things exploded (${e.message})`,
        };
      } else {
        setMessage("An error occured");
      }
    }
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-md-6 offset-md-3">
          <h3>Create a Blog Post</h3>
          <form onSubmit={(e) => handleSubmit(e)}>
            <div className="mb-3">
              <label htmlFor="topic" className="form-label">
                Topic
              </label>
              <input
                type="text"
                className="form-control"
                id="topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
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
          {message && (
            <div className={`alert alert-${messageType} mt-3`}>{message}</div>
          )}
        </div>
      </div>
      <BlogTable blogs={blogs} />
    </div>
  );
}

export default App;
