data "aws_iam_policy_document" "join_room_lambda" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "join_room_lambda_access_doc" {
  statement {
    actions = [
      "dynamodb:BatchGetItem",
      "dynamodb:DeleteItem",
      "dynamodb:DescribeTable",
      "dynamodb:GetItem",
      "dynamodb:GetRecords",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:UpdateItem",
    ]

    resources = [
      "${aws_dynamodb_table.signalws-hotel.arn}",
    ]
  }

  statement {
    actions = [
      "execute-api:ManageConnections",
    ]
    
    resources = [
      "arn:aws:execute-api:${var.region}:${var.account_id}:${var.websocket_api_id}/*"
    ]
  }

  statement {
    actions = [
      "autoscaling:Describe*",
      "cloudwatch:*",
      "logs:*",
      "sns:*",
      "iam:GetPolicy",
      "iam:GetPolicyVersion",
      "iam:GetRole",
    ]

    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "iam:CreateServiceLinkedRole",
    ]

    resources = [
      "arn:aws:iam::*:role/aws-service-role/events.amazonaws.com/AWSServiceRoleForCloudWatchEvents*",
    ]

    condition {
      test     = "StringLike"
      variable = "iam:AWSServiceName"

      values = [
        "events.amazonaws.com",
      ]
    }
  }
}

resource "aws_iam_policy" "join_room_lambda_access" {
  name   = "join_room_lambda_access"
  policy = "${data.aws_iam_policy_document.join_room_lambda_access_doc.json}"
}

resource "aws_iam_role_policy_attachment" "join_room_lambda_dynamo_policy_attach" {
  role       = "${aws_iam_role.iam_for_join_room_lambda.name}"
  policy_arn = "${aws_iam_policy.join_room_lambda_access.arn}"
}

resource "aws_iam_role" "iam_for_join_room_lambda" {
  name               = "join_room_iam"
  assume_role_policy = "${data.aws_iam_policy_document.join_room_lambda.json}"
}

resource "aws_lambda_function" "join_room" {
  filename         = "join_room.zip"
  function_name    = "join_room"
  runtime          = "python3.6"
  handler          = "join_room.lambda_handler"
  role             = "${aws_iam_role.iam_for_join_room_lambda.arn}"
  source_code_hash = "${base64sha256(file("join_room.zip"))}"
  timeout = 15
}
