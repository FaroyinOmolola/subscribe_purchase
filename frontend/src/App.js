import React from 'react';
import { PaystackButton } from 'react-paystack';
import './App.css';
const PAYSTACK_PUBLIC_KEY = 'pk_test_59330a42bd32d9c3e45b2cbef14f3d1e6cd7b3d1';

const config = {
  reference: new Date().getTime().toString(),
  email: 'omolola@gmail.com',
  amount: 20 * 100,
  publicKey: PAYSTACK_PUBLIC_KEY,
};

function App() {
  const handlePaystackSuccessAction = (reference) => console.log(reference);

  // you can call this function anything
  const handlePaystackCloseAction = () => console.log('closed');

  const componentProps = {
    ...config,
    text: 'Add Payment method',
    onSuccess: (reference) => handlePaystackSuccessAction(reference),
    onClose: handlePaystackCloseAction,
  };

  return (
    <div className='App'>
      <PaystackButton {...componentProps} />
    </div>
  );
}

export default App;
