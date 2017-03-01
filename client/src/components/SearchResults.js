import React, {Component} from 'react';
import {
  Grid,
  Row,
} from 'react-bootstrap';
import Message from './Message';

class SearchResults extends Component {
  render() {
    const messages = this.props.messages.map((message) => {
      return (<Message key={message.update_id} data={message} />);
    });

    return (
      <Grid>
        <Row>
          <h1>Search Results</h1>
        </Row>
        {messages.length ? messages : <p>No messages found</p>}
      </Grid>
    );
  }
}

export default SearchResults;
