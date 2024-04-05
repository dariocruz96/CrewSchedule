import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TestComponent = () => {
  const [rotas, setRotas] = useState([]);

  useEffect(() => {
    fetchRotas();
  }, []);

  const fetchRotas = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/rota/');
      setRotas(response.data);
    } catch (error) {
      console.error('Error fetching rotas:', error);
    }
  };

  return (
    <div>
      <h1>All Rotas</h1>
      <table border="1">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Shift</th>
            <th>Date Assigned</th>
          </tr>
        </thead>
        <tbody>
          {rotas.map((rota) => (
            <tr key={rota.id}>
              <td>{rota.employee.firstName} {rota.employee.lastName}</td>
              <td>{rota.shift.start_time} - {rota.shift.end_time}</td>
              <td>{rota.date_assigned}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TestComponent;
