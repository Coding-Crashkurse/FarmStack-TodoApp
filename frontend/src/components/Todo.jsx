import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";

const Todo = () => {
  return (
    <>
      <div className="todos done">
        <p>Todotext</p>
        <FontAwesomeIcon icon={faTrash} />
      </div>
    </>
  );
};

export default Todo;
