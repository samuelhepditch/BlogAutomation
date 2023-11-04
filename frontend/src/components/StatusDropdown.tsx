import React, { useState } from "react";
import { BlogStatus } from "../data/BlogStatus";

type DropdownProps = {
  updateBlogStatus: (value: BlogStatus) => void;
};

const StatusDropDown: React.FC<DropdownProps> = (props) => {
  const [selectedValue, setSelectedValue] = useState<BlogStatus>(
    BlogStatus.draft
  );

  const handleDropdownChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value as BlogStatus;
    setSelectedValue(value);

    props.updateBlogStatus(value);
  };

  return (
    <select
      className="form-select"
      value={selectedValue}
      onChange={handleDropdownChange}
    >
      <option value={BlogStatus.draft}>Draft</option>
      <option value={BlogStatus.publish}>Publish</option>
    </select>
  );
};

export default StatusDropDown;
