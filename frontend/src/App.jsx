import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [listName, setListName] = useState(""); // State for list name
  const [items, setItems] = useState([]); // State for items

  useEffect(() => {
    const fetchData = async () => {
      try {
        const todoListsResponse = await fetch(`${import.meta.env.VITE_API_URL}/todo-lists/1`); // Update with your endpoint
        const todoListsData = await todoListsResponse.json();
        setListName(todoListsData);
        console.log("list name:", listName.name);
        // Fetch Items
        const itemsResponse = await fetch(`${import.meta.env.VITE_API_URL}/todo-items/1`); // Update with your endpoint
        const itemsData = await itemsResponse.json();
        setItems(itemsData);
      
      } 
      catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);
const handleSave = async (e) => {
  e.preventDefault();
  console.log('handleSave called');

  const updatedItems = items.map((item) => {
    const checkbox = e.target[`c${item.id}`];
    console.log(`Processing item id ${item.id}, checkbox value:`, checkbox?.checked);
    return {
      id: item.id,
      todolist: 1,
      text: item.text,
      complete: checkbox ? checkbox.checked : false,
      duration: item.duration,
    };
  });

  try {
    console.log('Payload to send:', updatedItems);
    const response = await axios.put(
      `${import.meta.env.VITE_API_URL}/todo-items/1/`, // Update the endpoint if needed
      updatedItems,
      {
        headers: { 'Content-Type': 'application/json' }, // Set proper headers
      }
    );
    console.log('Items updated successfully:', response.data);
    window.location.reload();
  } 
  catch (error) {
    console.error('Error updating items:', error.message, error.response?.data);
  }
};
  return (
    <div>
      <h1>{listName.name}</h1>
      <form onSubmit={handleSave}>
        <ol>
          {items.map((item) => (
            <li key={item.id}>
              <label>
                <input
                  type="checkbox"
                  name={`c${item.id}`}
                  defaultChecked={item.complete}
                />
                {item.text}
              </label>
              {!item.complete && (
                      <>
                      <br /> 
                      <span>Duration: {item.duration}</span>
                      </>
                  )}
            </li>
          ))}
        </ol>
        <button type="submit" name="save" value="save">
          Save
        </button>
      </form>
    </div>
  );
}

export default App;
