import React, {Component} from 'react';
import {
  Grid,
  Row,
  Col,
  Form,
  FormGroup,
  ControlLabel,
  FormControl,
  Button,
  Alert
} from 'react-bootstrap';
import $ from 'jquery';
import SearchResults from './components/SearchResults';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      q: "",
      username: "",
      date: "",
      messages: [],
      errors: [],
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  doSearch() {
    $.ajax({
      type: "GET",
      data: {
        "q": this.state.q,
        "username": this.state.username,
        "date": this.state.date,
      },
      // TODO: configure URL
      url: 'http://localhost:8080/transcript/message/search',
      success: function (response) {
        if (response.success) {
          this.setState({
            messages: response.messages,
            errors: []
          });
        } else {
          this.setState({
            messages: [],
            errors: response.errors
          });
        }
      }.bind(this),
      error: function (jqXHR, textStatus, errorThrown) {
        let errors = this.state.errors;
        errors.push(errorThrown);
        this.setState({errors: errors})
      }.bind(this)
    });
  }

  componentDidMount() {
    this.doSearch();
  }

  handleSubmit(e) {
    e.preventDefault();

    this.doSearch();
  }

  handleChange(e) {
    let data = {};
    data[e.target.name] = e.target.value;

    this.setState(data);
  }

  render() {
    const errors = this.state.errors.map((errorText, index) => {
      return (
        <Alert key={index} bsStyle="danger">
          {errorText}
        </Alert>
      );
    });

    return (
      <div>
        <Grid>
          <Row>
            {errors}
            <Form inline>
              <Col xs={3}>
                <FormGroup controlId="formInlineName">
                  <ControlLabel>Search text:</ControlLabel>{' '}
                  <FormControl type="text" name="q" value={this.state.q} onChange={this.handleChange} />
                </FormGroup>
              </Col>
              <Col xs={3}>
                <FormGroup controlId="formInlineUsername">
                  <ControlLabel>Username:</ControlLabel>{' '}
                  <FormControl type="text" name="username" value={this.state.username} onChange={this.handleChange} />
                </FormGroup>
              </Col>
              <Col xs={3}>
                <FormGroup controlId="formInlineEmail">
                  <ControlLabel>Date:</ControlLabel>{' '}
                  <FormControl type="date" name="date" value={this.state.date} onChange={this.handleChange} />
                </FormGroup>
              </Col>
              <Col xs={3}>
                <Button type="submit" onClick={this.handleSubmit}>
                  Search
                </Button>
              </Col>
            </Form>
          </Row>
        </Grid>

        <SearchResults messages={this.state.messages} />

      </div>
    );
  }
}

export default App;
