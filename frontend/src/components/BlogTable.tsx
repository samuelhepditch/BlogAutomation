import React from 'react';
import Blog from '../classes/Blog';


type BlogTableProps = {
  blogs: Array<Blog>
}

const BlogTable = (props: BlogTableProps) => {
  return (
    <table className="table mt-5">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Post Topic</th>
          <th scope="col">Post Keywords</th>
          <th scope="col">Status</th>
        </tr>
      </thead>
      <tbody>
        {props.blogs.map((blog, index) => (
          <tr key={index}>
            <th scope="row">{index + 1}</th>
            <td>{blog.topic}</td>
            <td>{blog.keywords}</td>
            <td>{blog.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default BlogTable;
