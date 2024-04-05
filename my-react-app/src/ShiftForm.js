// ShiftForm.js
import React, { useState } from 'react';

const ShiftForm = ({ onSubmit, initialValues, onCancel }) => {
  const [formData, setFormData] = useState(initialValues || {});

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({});
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Employee:
        <input
          type="text"
          name="employee"
          value={formData.employee || ''}
          onChange={handleChange}
        />
      </label>
      <label>
        Start Time:
        <input
          type="datetime-local"
          name="start_time"
          value={formData.start_time || ''}
          onChange={handleChange}
        />
      </label>
      <label>
        End Time:
        <input
          type="datetime-local"
          name="end_time"
          value={formData.end_time || ''}
          onChange={handleChange}
        />
      </label>
      <button type="submit">{initialValues ? 'Update' : 'Add'}</button>
      {onCancel && <button onClick={onCancel}>Cancel</button>}
    </form>
  );
};

export default ShiftForm;
