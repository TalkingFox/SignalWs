provider "aws" {
  region = "${var.region}"
}

resource "aws_dynamodb_table" "signalrooms" {
  name           = "SignalRooms"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "roomName"

  attribute = [
    {
      name = "roomName"
      type = "S"
    }
  ]
}

resource "aws_dynamodb_table" "signalhosts" {
  name           = "SignalHosts"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "host"

  attribute = [
    {
      name = "host"
      type = "S"
    }
  ]
}

resource "aws_dynamodb_table" "signalwords" {
  name           = "SignalWords"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "wordsProperty"

  attribute = [
    {
      name = "wordsProperty"
      type = "S"
    },
  ]
}

resource "aws_dynamodb_table_item" "state_init" {
  table_name = "${aws_dynamodb_table.signalwords.name}"
  hash_key   = "${aws_dynamodb_table.signalwords.hash_key}"

  item = <<ITEM
    {        
        "wordsProperty": {
            "S": "wordsInUse"
        },
        "propertyValue": {
            "L": []
        }
    }
    ITEM
}
