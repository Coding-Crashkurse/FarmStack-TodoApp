import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";

const Todo = ({ description, done, id, onChangeTodo, onDeleteTodo }) => {
  return (
    <>
      <div className={"todos " + (done ? "done" : "")}>
        <p
          onClick={() => {
            onChangeTodo(id);
          }}
        >
          {description}
        </p>
        <FontAwesomeIcon
          icon={faTrash}
          onClick={() => {
            onDeleteTodo(id);
          }}
        />
      </div>
    </>
  );
};

export default Todo;
