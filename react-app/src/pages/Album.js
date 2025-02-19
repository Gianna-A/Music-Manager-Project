/**
 * @todo
 * this will be a page that will display a single album
 */

import { API } from "../constants";
import { useQuery } from '@tanstack/react-query';
import { Col, Container, Row } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import { useParams } from "react-router-dom";
import { Breadcrumb } from "react-bootstrap";
import { Link } from "react-router-dom";

const Album = () => {
    const {id} = useParams();
    const { isPending, data, error } = useQuery({
		queryKey: ['SingleAlbum'],
		queryFn: async () => {
			const response = await fetch(`${API}albums/${id}/`)
			return await response.json();
		},
	})
    if (isPending) return 'Loading...'

	if (error) return 'An error occurred here: ' + error.message

	console.log(data)

        function cover_image_route(str, API) {
            return API.slice(0,21) + str.slice(21)
        }

        function total_time(tracks){
            const total = tracks.reduce((sum, track) => sum + track.length, 0);
            const mins = Math.floor(total/60);
            const seconds = total - (mins*60);
            return `${mins} min ${seconds} sec`;
        }
		return (
        <Container className="my-4">
        <Breadcrumb>
            <Breadcrumb.Item linkAs={Link} linkProps={{ to: "/" }}> Home </Breadcrumb.Item>
            {id && (<Breadcrumb.Item active> {data.title} </Breadcrumb.Item>)}
        </Breadcrumb>
             <Row className="justify-content-center mb-4">
                < Col xs={12} md={8}>
                    <Card>
                                <Card.Img variant="top" src={cover_image_route(data.cover_image, API )} alt={`${data.title} cover`} />
                                <Card.Body>
                                    <Card.Title><strong>{data.title}</strong></Card.Title>
                                    <Card.Text><strong>{data.tracks.length} songs - {total_time(data.tracks)}</strong></Card.Text>
                                    <Card.Text><strong>Price: </strong>£{data.price} ({new Date(data.release_date).getFullYear()})</Card.Text>
                                    <Card.Text><strong>Artist: </strong>{data.artist}</Card.Text>
                                    <Card.Text>{data.description}</Card.Text>
                                </Card.Body>
                            </Card>
                    </Col>
            </Row>

            <Row  className="justify-content-center mb-4">
                <Col xs={12} md={8}>
                <Card>
                    <Card.Body>
                        <Card.Title><strong>Tracklist</strong></Card.Title>
                        {data.tracks.length === 0 ? (
                            <Card.Text>No Songs</Card.Text>
                        ) : (
                            data.tracks.map((track, index) => (
                            <Card.Text key={track.id}>{index + 1}. {track.title} - {track.length}s</Card.Text>
                        ))
                        )}
                    </Card.Body>
                </Card>
                </Col>
            </Row>

        </Container>

        
    );

}
export default Album