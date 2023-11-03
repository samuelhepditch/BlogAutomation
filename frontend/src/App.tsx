import React from "react";
import { useState } from "react";
import axios from "axios";
import BlogTable from "./components/BlogTable";
import Blog from "./data/Blog";
import "bootstrap/dist/css/bootstrap.min.css";
import { BlogService } from "./backend/BlogService";
import { RequestStatus } from "./data/RequestStatus";
import InputForm from "./components/InputForm";
import StatusDropDown from "./components/StatusDropdown";
import { BlogStatus } from "./data/BlogStatus";

function App() {
  const [message, setMessage] = useState<string>("");
  const [showMessage, setshowMessage] = useState(false);
  const [blogs, setBlogs] = useState<Array<Blog>>([]);

  const addBlog = (
    blogIndex: number,
    blogTitle: string,
    blogKeywords: string,
    blogStatus: BlogStatus
  ) => {
    let newBlog: Blog = new Blog(
      blogIndex,
      blogTitle,
      blogKeywords,
      RequestStatus.in_progress,
      blogStatus
    );

    setBlogs((prevBlogs) => [...prevBlogs, newBlog]);
  };

  const updateBlogStatus = (blogIndex: number, status: RequestStatus) => {
    setBlogs((prevBlogs) => {
      const updatedBlogs = [...prevBlogs];
      updatedBlogs[blogIndex].requestStatus = status;
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
        setMessage={setMessage}
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
