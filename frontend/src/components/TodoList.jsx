import React from "react";
import Todo from "./Todo";

const TodoList = () => {
  return (
    <>
      <div className="todo-wrapper">
        <div className="header-wrapper">
          <h1>Todo App</h1>
        </div>
        <Todo />
        <Todo />
        <Todo />
        <Todo />
        <div className="buttom-wrapper">
          <p>Du hast 4 offene Todos</p>
          <button className="delete-all">Alle Todos löschen!</button>
        </div>
      </div>
    </>
  );
};

export default TodoList;
