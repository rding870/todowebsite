import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [listName, setListName] = useState({}); // Default to an empty object to avoid errors
  const [items, setItems] = useState([]); // State for items

  // Fetch data when the component mounts
  useState(() => {
    const fetchData = async () => {
      try {
        // Fetch the list name
        const todoListsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/todo-lists/`);
        const todoListsData = todoListsResponse.data;
        setListName(todoListsData);
        console.log("List name:", todoListsData);
        // Fetch the items
        const itemsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/todo-items/`);
        const itemsData = itemsResponse.data;
        setItems(itemsData);
        console.log("Items:", itemsData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  // Handle saving the updated items
  const handleSave = async (e) => {
    e.preventDefault();
    console.log("handleSave called");

    // Collect updated data from checkboxes
    const updatedItems = items.map((item) => {
      const checkbox = document.querySelector(`input[name="c${item.id}"]`);
      console.log(`Processing item id ${item.id}, checkbox value:`, checkbox?.checked);
      return {
        id: item.id,
        todolist: 1, // Assuming todolist ID is 1; adjust as needed
        text: item.text,
        complete: checkbox ? checkbox.checked : false,
        duration: item.duration,
      };
    });

    try {
      // Update items in the API
      console.log("Payload to send:", updatedItems);
      const response = await axios.put(
        `${import.meta.env.VITE_API_URL}/todo-items/`,
        updatedItems,
        { headers: { "Content-Type": "application/json" } }
      );
      console.log("Items updated successfully:", Object.keys(response.data));
      setItems(response.data); // Update state with the response
    } catch (error) {
      console.error("Error updating items:", error.message, error.response?.data);
    }
  };

  // Handle deleting an item
  const handleDelete = async (idToRemove) => {
    console.log("handleDelete called for item id:", idToRemove);

    try {
      // Send DELETE request to the API
      await axios.delete(`${import.meta.env.VITE_API_URL}/todo-items/${idToRemove}/`);

      // Log success
      console.log(`Item with id ${idToRemove} deleted successfully.`);

      // Update local state to remove the deleted item
      setItems((prevItems) => prevItems.filter((item) => item.id !== idToRemove));
    } catch (error) {
      console.error("Error deleting item:", error.message, error.response?.data);
    }
  };

  return (
    <div>
      <h1>{listName[0]?.name }</h1>
      <form onSubmit={handleSave}>
        <ol>
          {items.map((item) => (
            <li key={item.id}>
              <label>
                <input type="checkbox" name={`c${item.id}`} defaultChecked={item.complete}/>
                {item.text}
                <button type="button" onClick={() => handleDelete(item.id)}>
                  Delete
                </button>
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
        <button type="submit">Save</button>
      </form>
    </div>
  );
}

export default App;
