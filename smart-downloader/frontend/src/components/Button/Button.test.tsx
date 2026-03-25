import React from 'react';
import { Button, PrimaryButton, DangerButton } from './index';
import { render, screen } from '@testing-library/react';

describe('Button Component', () => {
  it('renders basic button', () => {
    render(<Button>Click Me</Button>);
    
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });

  it('renders primary button with type primary', () => {
    render(<PrimaryButton>Primary</PrimaryButton>);
    
    const button = screen.getByText('Primary');
    expect(button).toBeInTheDocument();
  });

  it('renders danger button', () => {
    render(<DangerButton>Danger</DangerButton>);
    
    expect(screen.getByText('Danger')).toBeInTheDocument();
  });

  it('passes through props correctly', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    
    screen.getByText('Click').click();
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('renders loading state', () => {
    render(<Button loading>Loading</Button>);
    
    expect(screen.getByText('Loading')).toBeInTheDocument();
  });
});
