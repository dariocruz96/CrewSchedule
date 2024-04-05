import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const HomePage = () => {
  const [data, setData] = useState([]);
  const [shifts, setShifts] = useState([]);
  const days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  useEffect(() => {
    fetchData();
    fetchShifts(); // Fetch shifts data
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/employee/');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchShifts = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/shifts/');
      setShifts(response.data);
    } catch (error) {
      console.error('Error fetching shifts:', error);
    }
  };

  const handleDragEnd = async result => {
    if (!result.destination) {
      return;
    }
  
    // Rearrange the order of team members in the state
    const newData = Array.from(data);
    const [removed] = newData.splice(result.source.index, 1);
    newData.splice(result.destination.index, 0, removed);
    setData(newData);
  
    try {
      await axios.post('http://127.0.0.1:8000/api/update-shifts', newData);
    } catch (error) {
      console.error('Error updating shifts:', error);
    }
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <table border="1">
        <thead>
          <tr>
            <th>Employee</th>
            {days_of_week.map(day => (
              <th key={day}>{day}</th>
            ))}
          </tr>
        </thead>
        <Droppable droppableId="employees">
          {(provided) => (
            <tbody {...provided.droppableProps} ref={provided.innerRef}>
              {data.map((employee, index) => (
                <Draggable key={employee.id} draggableId={employee.id} index={index}>
                  {(provided) => (
                    <tr
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                    >
                      <td>{employee.firstName} {employee.lastName}</td>
                      {days_of_week.map(day => (
                        <td key={`${employee.id}-${day}`}>
                          {shifts.map(shift => (
                            (shift.employee === employee.id && shift.day_of_week === day) ?
                              `${shift.start_time} - ${shift.end_time}` :
                              null
                          ))}
                        </td>
                      ))}
                    </tr>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </tbody>
          )}
        </Droppable>
      </table>
    </DragDropContext>
  );
};

export default HomePage;
