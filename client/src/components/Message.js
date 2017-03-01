import React, {Component} from 'react';
import {
  Row,
  Col,
  Panel,
} from 'react-bootstrap';

class Message extends Component {
  render() {
    const date = new Date(this.props.data.date);
    let fromName;

    if (this.props.data.chat_type === 'group') {
      fromName = (
        <span>
          <b>{this.props.data.from_username}</b>
          {" in group "}
          <b>{this.props.data.chat_name}</b>
        </span>
      );
    } else if (this.props.data.chat_type === 'channel') {
      fromName = (
        <span>
          <b>{this.props.data.chat_name}</b>
        </span>
      );
    } else {
      fromName = (<b>{this.props.data.from_username}</b>);
    }

    const title = (
      <div>
        {fromName}
        <b className="pull-right">{date.toLocaleString()}</b>
      </div>
    );

    return (
      <Row>
        <Col xs={12}>
          <Panel header={title}>
            {this.props.data.text}
          </Panel>
        </Col>
      </Row>
    );
  }
}

export default Message;
