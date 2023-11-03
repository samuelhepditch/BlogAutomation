import React from "react";
import { useState } from "react";
import axios from "axios";
import BlogTable from "./components/BlogTable";
import Blog from "./data/Blog";
import "bootstrap/dist/css/bootstrap.min.css";
import { BlogService } from "./backend/BlogService";
import { BlogStatus } from "./data/BlogStatus";
import InputForm from "./components/InputForm";

function App() {
  const [blogTitle, setBlogTitle] = useState<string>("");
  const [keywords, setKeywords] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [showMessage, setshowMessage] = useState(false);
  const [blogs, setBlogs] = useState<Array<Blog>>([]);

  const addBlog = (blogIndex: number) => {
    let newBlog: Blog = new Blog(
      blogIndex,
      blogTitle,
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

  const udpateBlogNotes = (blogIndex: number, message: string) => {
    setBlogs((prevBlogs) => {
      const updatedBlogs = [...prevBlogs];
      updatedBlogs[blogIndex].notes = message;
      return updatedBlogs;
    });
  };

  // Function to show the alert
  const showAlertHandler = () => {
    setshowMessage(true);
  };

  // Function to hide the alert
  const hideAlertHandler = () => {
    setshowMessage(false);
  };

  return (
    <div className="container mt-5">
      <InputForm
        addBlog={addBlog}
        blogs={blogs}
        udpateBlogNotes={udpateBlogNotes}
        updateBlogStatus={updateBlogStatus}
        hideAlertHandler={hideAlertHandler}
        showAlertHandler={showAlertHandler}
      />
      <br />
      {showMessage && (
        <div className="alert">
          <p>{message}</p>
          <button onClick={hideAlertHandler}>Close</button>
        </div>
      )}
      <br />
      <BlogTable blogs={blogs} />
    </div>
  );
}

export default App;
