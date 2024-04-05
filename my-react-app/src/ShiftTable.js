// ShiftTable.js
import React from 'react';

const ShiftTable = ({ shifts, onEdit, onDelete }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Employee</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {shifts.map((shift) => (
          <tr key={shift.id}>
            <td>{shift.employee.name}</td>
            <td>{shift.start_time}</td>
            <td>{shift.end_time}</td>
            <td>
              <button onClick={() => onEdit(shift)}>Edit</button>
              <button onClick={() => onDelete(shift.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ShiftTable;
