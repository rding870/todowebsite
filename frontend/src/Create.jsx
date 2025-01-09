import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Create() {
  const [formData, setFormData] = useState({
    task: "",
    complete: false,
    duration: "",
  });

  const navigate = useNavigate(); // For navigating to another page
  const handleBack = () => {
    // Redirect to the desired page
    navigate('/');
  };
  // Handle form input changes
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/todo-items/create/`,
        {
          task: formData.task,
          complete: formData.complete,
          duration: formData.duration,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      console.log("Task created successfully:", response.data);

      // Navigate to another page (e.g., task list page)
      navigate("/");
    } catch (error) {
      console.error("Error creating task:", error);
    }
  };

  return (
    <div>
      <h1>Create a New Task</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Task:
            <input
              type="text"
              name="task"
              value={formData.task}
              onChange={handleChange}
              required
            />
          </label>
        </div>
        <div>
          <label>
            Complete:
            <input
              type="checkbox"
              name="complete"
              checked={formData.complete}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            Duration:
            <input
              type="text"
              name="duration"
              value={formData.duration}
              onChange={handleChange}
              placeholder="e.g., 00:30:00"
              required
            />
          </label>
        </div>
        <button type="submit">Create Task</button>
        <button type="button" onClick={() => handleBack()}> Back </button>
      </form>
    </div>
  );
}

export default Create;
