data "aws_iam_policy_document" "delete_room_lambda" {
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

data "aws_iam_policy_document" "delete_room_lambda_access_doc" {
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

resource "aws_iam_policy" "delete_room_lambda_access" {
  name   = "delete_room_lambda_access"
  policy = "${data.aws_iam_policy_document.delete_room_lambda_access_doc.json}"
}

resource "aws_iam_role_policy_attachment" "delete_room_lambda_dynamo_policy_attach" {
  role       = "${aws_iam_role.iam_for_delete_room_lambda.name}"
  policy_arn = "${aws_iam_policy.delete_room_lambda_access.arn}"
}

resource "aws_iam_role" "iam_for_delete_room_lambda" {
  name               = "delete_room_iam"
  assume_role_policy = "${data.aws_iam_policy_document.delete_room_lambda.json}"
}

resource "aws_lambda_function" "delete_room" {
  filename         = "delete_room.zip"
  function_name    = "delete_room"
  runtime          = "python3.6"
  handler          = "delete_room.lambda_handler"
  role             = "${aws_iam_role.iam_for_delete_room_lambda.arn}"
  source_code_hash = "${base64sha256(file("delete_room.zip"))}"
}
