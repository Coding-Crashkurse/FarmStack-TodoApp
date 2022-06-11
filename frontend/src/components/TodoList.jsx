import React from "react";
import Todo from "./Todo";
import { useState, useRef, useEffect } from "react";
import axios from "axios";

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [token, setToken] = useState("");
  const [loggedIn, setloggedIn] = useState(false);
  const [opencount, countOpen] = useState(todos.length);
  const [loginError, setloginError] = useState(false);
  const [registerError, setregisterError] = useState(false);
  const [registerSuccess, setregisterSuccess] = useState(false);

  const usernameRef = useRef();
  const passwordRef = useRef();
  const todoInputRef = useRef();

  useEffect(() => {
    const donetodos = todos.filter((item) => {
      return !item.done;
    });
    countOpen(donetodos.length);
  }, [todos]);

  const register = () => {
    axios
      .post("http://127.0.0.1:8000/register", {
        username: usernameRef.current.value,
        password: passwordRef.current.value,
      })
      .then((res) => {
        setregisterSuccess(true);
        setTimeout(() => {
          setregisterSuccess(false);
        }, 1500);
      })
      .catch((err) => {
        setregisterError(true);
        setTimeout(() => {
          setregisterError(false);
        }, 1500);
      });
  };

  const login = () => {
    let data = new FormData();
    data.append("username", usernameRef.current.value);
    data.append("password", passwordRef.current.value);

    axios
      .post("http://127.0.0.1:8000/login", data)
      .then((res) => {
        setToken(res.data.access_token);
        getAllTodos(res.data.access_token);
        setloggedIn(true);
      })
      .catch((err) => {
        setloginError(true);
        setTimeout(() => {
          setloginError(false);
        }, 1500);
      });
  };

  const logout = () => {
    setToken("");
    setloggedIn(false);
  };

  const getAllTodos = (access_token) => {
    axios
      .get("http://127.0.0.1:8000/get_todos_by_user", {
        headers: { Authorization: `Bearer ${access_token}` },
      })
      .then((res) => {
        setTodos(res.data);
      });
  };

  const addTodo = () => {
    axios
      .post(
        "http://127.0.0.1:8000/create_todo",
        {
          description: todoInputRef.current.value,
          done: false,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      .then(() => {
        getAllTodos(token);
        todoInputRef.current.value = "";
      });
  };

  const delete_todo = (id) => {
    axios
      .delete(`http://127.0.0.1:8000/delete_todo/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => {
        getAllTodos(token);
      });
  };

  const update_todo = (id) => {
    axios
      .put(
        `http://127.0.0.1:8000/update_todo/${id}`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      .then(() => {
        getAllTodos(token);
      });
  };

  return (
    <>
      <div className="todo-wrapper">
        <h1>Login/Register</h1>
        <input type="text" placeholder="username" ref={usernameRef} />
        <input type="text" placeholder="password" ref={passwordRef} />
        <div className="regloginbtns">
          <button className="btn" onClick={register}>
            Registrierung
          </button>
          <button className="btn" onClick={login}>
            Login
          </button>
        </div>
        {registerError ? <p className="error">User existiert bereits</p> : ""}
        {registerSuccess ? (
          <p className="success">Registrierung erfolgreich!</p>
        ) : (
          ""
        )}
        {loginError ? <p className="error">Login fehlgeschlagen</p> : ""}
      </div>

      <div className={loggedIn ? "todo-wrapper" : "hidden"}>
        <div className="header-wrapper">
          <h1>Todo App</h1>
        </div>
        <div className="input-wrapper">
          <input type="text" placeholder="Neues Todo..." ref={todoInputRef} />
          <button className="btn" onClick={addTodo}>
            Todo hinzufügen
          </button>
        </div>
        {todos.map((item, index) => {
          return (
            <Todo
              key={index}
              description={item.description}
              done={item.done}
              id={item._id}
              onChangeTodo={update_todo}
              onDeleteTodo={delete_todo}
              index={index}
            />
          );
        })}
        <div className="buttom-wrapper">
          <p>Du hast {opencount} offene Todos</p>
          <button className="btn" onClick={logout}>
            Logout
          </button>
        </div>
      </div>
    </>
  );
};

export default TodoList;
