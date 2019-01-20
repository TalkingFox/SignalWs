data "aws_iam_policy_document" "add_to_room_lambda" {
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

data "aws_iam_policy_document" "add_to_room_lambda_access_doc" {
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

resource "aws_iam_policy" "add_to_room_lambda_access" {
  name   = "add_to_room_lambda_access"
  policy = "${data.aws_iam_policy_document.add_to_room_lambda_access_doc.json}"
}

resource "aws_iam_role_policy_attachment" "add_to_room_lambda_dynamo_policy_attach" {
  role       = "${aws_iam_role.iam_for_add_to_room_lambda.name}"
  policy_arn = "${aws_iam_policy.add_to_room_lambda_access.arn}"
}

resource "aws_iam_role" "iam_for_add_to_room_lambda" {
  name               = "add_to_room_iam"
  assume_role_policy = "${data.aws_iam_policy_document.add_to_room_lambda.json}"
}

resource "aws_lambda_function" "add_to_room" {
  filename         = "add_to_room.zip"
  function_name    = "add_to_room"
  runtime          = "python3.6"
  handler          = "add_to_room.lambda_handler"
  role             = "${aws_iam_role.iam_for_add_to_room_lambda.arn}"
  source_code_hash = "${base64sha256(file("add_to_room.zip"))}"
  timeout = 15
}
