/**
 * @todo
 * this will be a page that will display a list of albums
 */
import { API } from "../constants";
import { useQuery } from '@tanstack/react-query';
import { Col, Container, Row } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import { Link } from "react-router-dom";


const Home = () => {
    const { isPending, data, error } = useQuery({
		queryKey: ['AlbumData'],
		queryFn: async () => {
			const response = await fetch(`${API}albums/`)
			return await response.json();
		},
	})
    if (isPending) return 'Loading...'

	if (error) return 'An error occurred here: ' + error.message

	console.log(data)

        function shorten_description(str) {
            if (str.length >= 255) {
                return  str.slice(0, 255)+ "...";
            } else {
                return str;
            }
        }

        function cover_image_route(str, API) {
            return API.slice(0,21) + str.slice(21)
        }
		return (
        <Container className="my-4">
            <Row className="g-4">
                {data.map(album => (<Col key={album.id} xs={12} md={4}>
                        <Link to={`/albums/${album.id}`} style={{ textDecoration: "none" }}>
                            <Card className="h-100">
                                <Card.Img variant="top" src={cover_image_route(album.cover_image, API )} alt={`${album.title} cover`} />
                                <Card.Body>
                                    <Card.Title>{album.title}</Card.Title>
                                    <Card.Text>Artist: {album.artist}</Card.Text>
                                    <Card.Text>{shorten_description(album.description)}</Card.Text>
                                    <Card.Text>Price: £{album.price} ({new Date(album.release_date).getFullYear()})</Card.Text>
                                </Card.Body>
                            </Card>
                        </Link>
                    </Col>
                ))}
            </Row>
        </Container>
    );

}
export default Home