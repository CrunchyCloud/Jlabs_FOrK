import './Main.css';
import { useNavigate } from 'react-router-dom';

const Main = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/signin'); // Adjust the path as needed
  };

  return (
    <div>
      <button onClick={handleRedirect}>Go to Sign In</button>
    </div>
  );
};

export default Main;

