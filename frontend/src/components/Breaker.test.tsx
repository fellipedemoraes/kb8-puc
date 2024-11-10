import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Breaker from './Breaker';
import React from 'react';

test('renders Breaker component', () => {
  render(<Breaker />);
  const breakerComponent = screen.getByText(/Guess the Word/i);
  expect(breakerComponent).toBeInTheDocument();
});
// Import FetchMock type
import { FetchMock } from 'jest-fetch-mock';

// Create fetch constant with correct type
const fetch = global.fetch as FetchMock;

test('submits guess and displays result', async () => {
  fetch.mockResponseOnce(JSON.stringify({ result: 'Correct' }));

  const { getByLabelText, getByText, getByRole } = render(<Breaker />);

  fireEvent.change(getByLabelText(/game id/i), { target: { value: '1' } });
  fireEvent.change(getByLabelText(/your guess/i), { target: { value: 'apple' } });
  fireEvent.click(getByRole('button', { name: /submit guess/i }));

  await waitFor(() => getByText(/result: correct/i));
});

test('handles 404 error when game is not found', async () => {
  fetch.mockResponseOnce(JSON.stringify({ error: 'Game not found' }), { status: 404 });

  const { getByLabelText, getByText, getByRole } = render(<Breaker />);

  fireEvent.change(getByLabelText(/game id/i), { target: { value: '1' } });
  fireEvent.change(getByLabelText(/your guess/i), { target: { value: 'apple' } });
  fireEvent.click(getByRole('button', { name: /submit guess/i }));

  await waitFor(() => getByText(/Game not found/i));
});
