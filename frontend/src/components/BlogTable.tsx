import Blog from "../data/Blog";
import { RequestStatus } from "../data/RequestStatus";
import "../App.css";

type BlogTableProps = {
  blogs: Array<Blog>;
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
        </tr>
      </thead>
      <tbody>
        {props.blogs
          .slice()
          .reverse()
          .map((blog, index) => (
            <tr key={index}>
              <th scope="row">{blog.index}</th>
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
                    : ""
                }
              >
                {blog.requestStatus}
              </td>
              <td>{blog.notes}</td>
            </tr>
          ))}
      </tbody>
    </table>
  );
};

export default BlogTable;
