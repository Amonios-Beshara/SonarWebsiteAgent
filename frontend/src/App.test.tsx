import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders HelloSonar AI title', () => {
  render(<App />);
  const titleElement = screen.getByText(/HelloSonar AI/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders voice session button', () => {
  render(<App />);
  const buttonElement = screen.getByText(/Start Voice Session/i);
  expect(buttonElement).toBeInTheDocument();
});

test('renders voice agent description', () => {
  render(<App />);
  const descriptionElement = screen.getByText(/This is the voice agent that is going to help us write the documentation together/i);
  expect(descriptionElement).toBeInTheDocument();
});
