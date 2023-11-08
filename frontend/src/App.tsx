import { useState, useEffect } from "react";
import BlogTable from "./components/BlogTable";
import Blog from "./data/Blog";
import "bootstrap/dist/css/bootstrap.min.css";
import { RequestStatus } from "./data/RequestStatus";
import InputForm from "./components/InputForm";
import { BlogStatus } from "./data/BlogStatus";
import { BlogService } from "./backend/BlogService";

function App() {

  const [message, setMessage] = useState<string>("");
  const [showMessage, setShowMessage] = useState(false);
  const [failedToWrite, setFailedToWrite] = useState(false);
  const [blogQueue, setBlogQueue] = useState<Array<Blog>>([]);
  const [isSending, setIsSending] = useState(false);

  const blogService = new BlogService(true);

  const addBlogToQueue = (
    blogTitle: string,
    blogKeywords: string,
    blogStatus: BlogStatus
  ) => {
    const newBlog: Blog = new Blog(
      blogQueue.length,
      blogTitle,
      blogKeywords,
      RequestStatus.queued,
      blogStatus
    );
    setBlogQueue((prevQueue) => [...prevQueue, newBlog]);
  };

  const writeBlog = async (currentBlog: Blog) => {
    console.log("attempt")
    setIsSending(true);
    updateBlogStatus(currentBlog.index, RequestStatus.in_progress);
    try {
      const response = await blogService.writeBlog(
        currentBlog.topic,
        currentBlog.keywords,
        currentBlog.status
      );
      udpateBlogNotes(currentBlog.index, response.data.message);
      if (response.data.status === "error") {
        setFailedToWrite(true);
        updateBlogStatus(currentBlog.index, RequestStatus.failed);
      } else {
        setFailedToWrite(false);
        updateBlogStatus(currentBlog.index, RequestStatus.success);
      }
    } catch (e: unknown) {
      setFailedToWrite(true)
      updateBlogStatus(currentBlog.index, RequestStatus.failed);
      if (e instanceof Error) {
        udpateBlogNotes(currentBlog.index, e.message);
        setMessage(`Error in writeBlog: (${e})`);
      } else {
        setMessage(
          "An unknown exception occured when sending a request."
        );
      }
      showAlertHandler();
    } finally {
      setIsSending(false);
    }
  }

  const sendNextBlog = async () => {
    if (isSending || blogQueue.length === 0 || failedToWrite) {
      return;
    }
    for (const blog of blogQueue) {
      if (blog.requestStatus === RequestStatus.queued) {
        writeBlog(blog);
      }
    }
  };

  useEffect(() => {
    sendNextBlog();
  }, [blogQueue]); 

  const updateBlogStatus = (blogIndex: number, status: RequestStatus) => {
    setBlogQueue((prevQueue) => {
      const updatedBlogs = [...prevQueue];
      updatedBlogs[blogIndex].requestStatus = status;
      return updatedBlogs;
    });
  };

  const udpateBlogNotes = (blogIndex: number, message: string) => {
    setBlogQueue((prevQueue) => {
      const updatedBlogs = [...prevQueue];
      updatedBlogs[blogIndex].notes = message;
      return updatedBlogs;
    });
  };

  const onDequeue = (blogIndex: number) => {
    updateBlogStatus(blogIndex, RequestStatus.dequeued)
    sendNextBlog()
  };

  const onRetry = (blogIndex: number) => {
    console.log("retry")
    udpateBlogNotes(blogIndex, '');
    updateBlogStatus(blogIndex, RequestStatus.queued)
    setFailedToWrite(false);
    sendNextBlog();
  };

  const onSkip = (blogIndex: number) => {
    updateBlogStatus(blogIndex, RequestStatus.skipped);
    setFailedToWrite(false);
    sendNextBlog();
  };

  const showAlertHandler = () => {
    setShowMessage(true);
  };

  const hideAlertHandler = () => {
    setShowMessage(false);
  };
  
  return (
    <div className="container mt-5">
      <InputForm
        addBlogToQueue={addBlogToQueue}
        blogQueue={blogQueue}
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
      <BlogTable 
        blogs={blogQueue}
        onDequeue={onDequeue}
        onSkip={onSkip}
        onRetry={onRetry}
      />
    </div>
  );
}

export default App;
