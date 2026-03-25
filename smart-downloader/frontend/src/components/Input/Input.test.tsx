import React from 'react';
import { Input, PasswordInput, TextArea } from './index';
import { render, screen } from '@testing-library/react';

describe('Input Component', () => {
  it('renders basic input', () => {
    render(<Input placeholder="Enter text" />);
    
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
  });

  it('renders password input', () => {
    render(<PasswordInput placeholder="Enter password" />);
    
    expect(screen.getByPlaceholderText('Enter password')).toBeInTheDocument();
  });

  it('renders textarea', () => {
    render(<TextArea placeholder="Enter text" rows={4} />);
    
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
  });

  it('passes through value prop', () => {
    render(<Input value="test value" onChange={() => {}} />);
    
    expect(screen.getByDisplayValue('test value')).toBeInTheDocument();
  });

  it('handles change events', () => {
    const handleChange = jest.fn();
    render(<Input onChange={handleChange} />);
    
    screen.getByRole('textbox').value = 'new value';
    fireEvent.change(screen.getByRole('textbox'));
    
    expect(handleChange).toHaveBeenCalled();
  });
});
