import React from 'react';
import Blog from "../data/Blog";
import { RequestStatus } from "../data/RequestStatus";
import "../App.css";

type BlogTableProps = {
  blogs: Array<Blog>;
  onDequeue: (index: number) => void;
  onSkip: (index: number) => void;
  onRetry: (index: number) => void;
};

const BlogTable = (props: BlogTableProps) => {
  return (
    <table className="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Post Title</th>
          <th scope="col">Post Keywords</th>
          <th scope="col">Status</th>
          <th scope="col">Notes</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        {props.blogs
          .slice()
          .reverse()
          .map((blog, index) => (
            <tr key={index}>
              <th scope="row">{index}</th>
              <td>{blog.topic}</td>
              <td>{blog.keywords}</td>
              <td
                className={
                  blog.requestStatus === RequestStatus.success
                    ? "table-success"
                    : blog.requestStatus === RequestStatus.failed
                    ? "table-danger"
                    : blog.requestStatus === RequestStatus.in_progress
                    ? "table-info"
                    : blog.requestStatus === RequestStatus.queued
                    ? "table-secondary"
                    : blog.requestStatus === RequestStatus.skipped
                    ? "table-primary"
                    : blog.requestStatus === RequestStatus.dequeued
                    ? "table-warning"
                    : ""
                }
              >
                {blog.requestStatus}
              </td>
              <td>{blog.notes}</td>
              <td>
                {blog.requestStatus === RequestStatus.queued && (<button
                    style={{
                      marginRight: '10px',
                      marginBottom: '5px',
                      backgroundColor: '#f8d7da',
                      borderColor: '#f5c6cb',
                      color: '#721c24', 
                      padding: '5px 10px', 
                      width: '100px' 
                    }}
                    className="btn"
                    onClick={() => props.onDequeue(blog.index)}
                  >
                    Dequeue
                  </button>
                )}
                {blog.requestStatus === RequestStatus.failed && (<button
                    style={{
                      marginRight: '10px',
                      marginBottom: '5px',
                      backgroundColor: '#f8d7da',
                      borderColor: '#f5c6cb',
                      color: '#721c24', 
                      padding: '5px 10px', 
                      width: '100px' 
                    }}
                    className="btn"
                    onClick={() => props.onSkip(blog.index)}
                  >
                    Skip
                  </button>
                )}
                {blog.requestStatus === RequestStatus.failed && (
                  <button
                    style={{
                      backgroundColor: '#d6d8db',
                      borderColor: '#c6c8ca',
                      color: '#383d41',
                      padding: '5px 10px',
                      width: '100px'
                    }}
                    className="btn"
                    onClick={() => props.onRetry(index)}
                  >
                  Retry
                  </button>
                )}
              </td>
            </tr>
          ))}
      </tbody>
    </table>
  );
};

export default BlogTable;

