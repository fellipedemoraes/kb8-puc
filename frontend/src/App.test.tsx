import { render, screen } from '@testing-library/react';
import App from './App';
import React from 'react';

test('renders home link', () => {
  render(
    <App />
  );
  const homeLink = screen.getByText(/Home/i);
  expect(homeLink).toBeInTheDocument();
});

test('renders maker link', () => {
  render(
    <App />
  );
  const makerLink = screen.getByText(/Maker/i);
  expect(makerLink).toBeInTheDocument();
});

test('renders breaker link', () => {
  render(
    <App />
  );
  const breakerLink = screen.getByText(/Breaker/i);
  expect(breakerLink).toBeInTheDocument();
});
