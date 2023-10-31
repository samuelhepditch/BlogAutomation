import React from 'react';
import { useState } from "react";
import axios from "axios";
import BlogTable from "./components/BlogTable";
import "bootstrap/dist/css/bootstrap.min.css";
import Blog from './classes/Blog';

function App() {
  const [topic, setTopic] = useState<string>("");
  const [keywords, setKeywords] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [messageType, setMessageType] = useState<string>("");
  const [blogs, setBlogs] = useState<Array<Blog>>([]);

  const addBlog = () => {
    let copiedBlogs: Array<Blog> = [...blogs];

    let newBlog: Blog = new Blog(topic, keywords, "in progress");

    copiedBlogs.push(newBlog);

    setBlogs(copiedBlogs);
  };

  const handleSubmit = async () => {
    try {
      addBlog();
      const response = await axios.post("/write_blog", { topic, keywords });
      if (response.data.status === "error") {
        setMessage(response.data.message);
        setMessageType("error");
      } else {
        setMessage(response.data.message);
        setMessageType("success");
      }
    } catch (error) {
      console.error("There was an error submitting the form", error);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-md-6 offset-md-3">
          <h3>Create a Blog Post</h3>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="topic" className="form-label">Topic</label>
              <input type="text" className="form-control" id="topic" value={topic} onChange={(e) => setTopic(e.target.value)} required />
            </div>
            <div className="mb-3">
              <label htmlFor="keywords" className="form-label">Keywords (comma-separated)</label>
              <input type="text" className="form-control" id="keywords" value={keywords} onChange={(e) => setKeywords(e.target.value)} required />
            </div>
            <button type="submit" className="btn btn-primary">Write Blog Post</button>
          </form>
          {message && <div className={`alert alert-${messageType} mt-3`}>{message}</div>}
        </div>
      </div>
      <BlogTable blogs={blogs}/>
    </div>
  );
}

export default App;

