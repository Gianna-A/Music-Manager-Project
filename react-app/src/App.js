
import { Container } from 'react-bootstrap';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Album from './pages/Album';
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <Container>
      <Routes>
      <Route path="/">
        <Route index element={<Home />} />
        <Route path="/albums/:id" element={<Album />} />
      </Route>
    </Routes>

    </Container>
  );
  
}

export default App;
