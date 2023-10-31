import Blog from "../data/Blog";
import { BlogStatus } from "../data/BlogStatus";
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
          <th scope="col">Post Topic</th>
          <th scope="col">Post Keywords</th>
          <th scope="col">Status</th>
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
                  blog.status === BlogStatus.success
                    ? "table-success"
                    : blog.status === BlogStatus.failed
                    ? "table-danger"
                    : blog.status === BlogStatus.in_progress
                    ? "table-info"
                    : ""
                }
              >
                {blog.status}
              </td>
            </tr>
          ))}
      </tbody>
    </table>
  );
};

export default BlogTable;
