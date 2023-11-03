import React, { useState } from "react";
import { BlogState } from "../data/BlogState";

type DropdownProps = {
  updateBlogState: (value: BlogState) => void;
};

const StatusDropDown: React.FC<DropdownProps> = (props) => {
  const [selectedValue, setSelectedValue] = useState<BlogState>(
    BlogState.draft
  );

  const handleDropdownChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as BlogState;
    setSelectedValue(value);

    props.updateBlogState(value);
  };

  return (
    <select
      className="form-select"
      value={selectedValue}
      onChange={handleDropdownChange}
    >
      <option value={BlogState.draft}>Draft</option>
      <option value={BlogState.publish}>Publish</option>
    </select>
  );
};

export default StatusDropDown;
