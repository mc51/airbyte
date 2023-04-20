#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#


from typing import Mapping

import pytest
from airbyte_cdk import AirbyteLogger
from source_s3.s3_utils import AuthenticationMethod, get_authentication_method

LOGGER = AirbyteLogger()


class TestS3Utils:
    @pytest.mark.parametrize(  # passing in full provider to emulate real usage (dummy values are unused by func)
        "provider, authentication, expected_authentication_method",
        [
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "aws_secret_access_key": "key", "path_prefix": "dummy"},
                None,
                AuthenticationMethod.ACCESS_KEY_SECRET_ACCESS_KEY,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "aws_secret_access_key": "key", "path_prefix": "dummy"},
                {"auth_method": "aws_default_credentials"},
                AuthenticationMethod.ACCESS_KEY_SECRET_ACCESS_KEY,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "aws_secret_access_key": "key", "path_prefix": "dummy"},
                {"auth_method": "aws_provided_credentials"},
                AuthenticationMethod.ACCESS_KEY_SECRET_ACCESS_KEY,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "aws_secret_access_key": "key", "path_prefix": "dummy"},
                {"auth_method": "no_credentials"},
                AuthenticationMethod.ACCESS_KEY_SECRET_ACCESS_KEY,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": None, "aws_secret_access_key": None, "path_prefix": "dummy"},
                None,
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": None, "aws_secret_access_key": None, "path_prefix": "dummy"},
                {"auth_method": "aws_default_credentials"},
                AuthenticationMethod.DEFAULT,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": None, "aws_secret_access_key": None, "path_prefix": "dummy"},
                {"auth_method": "no_credentials"},
                AuthenticationMethod.UNSIGNED,
            ),
            ({"storage": "S3", "bucket": "dummy", "path_prefix": "dummy"}, None, AuthenticationMethod.UNSIGNED),
            (
                {"storage": "S3", "bucket": "dummy", "path_prefix": "dummy"},
                {"auth_method": "aws_default_credentials"},
                AuthenticationMethod.DEFAULT,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "path_prefix": "dummy"},
                {"auth_method": "no_credentials"},
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "aws_secret_access_key": None, "path_prefix": "dummy"},
                None,
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "aws_secret_access_key": None, "path_prefix": "dummy"},
                {"auth_method": "aws_default_credentials"},
                AuthenticationMethod.DEFAULT,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "aws_secret_access_key": None, "path_prefix": "dummy"},
                {"auth_method": "no_credentials"},
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": None, "aws_secret_access_key": "key", "path_prefix": "dummy"},
                None,
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": None, "aws_secret_access_key": "key", "path_prefix": "dummy"},
                {"auth_method": "aws_default_credentials"},
                AuthenticationMethod.DEFAULT,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": None, "aws_secret_access_key": "key", "path_prefix": "dummy"},
                {"auth_method": "no_credentials"},
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "path_prefix": "dummy"},
                None,
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "path_prefix": "dummy"},
                {"auth_method": "aws_default_credentials"},
                AuthenticationMethod.DEFAULT,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_access_key_id": "id", "path_prefix": "dummy"},
                {"auth_method": "no_credentials"},
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_secret_access_key": "key", "path_prefix": "dummy"},
                None,
                AuthenticationMethod.UNSIGNED,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_secret_access_key": "key", "path_prefix": "dummy"},
                {"auth_method": "aws_default_credentials"},
                AuthenticationMethod.DEFAULT,
            ),
            (
                {"storage": "S3", "bucket": "dummy", "aws_secret_access_key": "key", "path_prefix": "dummy"},
                {"auth_method": "no_credentials"},
                AuthenticationMethod.UNSIGNED,
            ),
        ],
    )
    def test_get_authentication_method(
        self, provider: Mapping[str, str], authentication: dict[str, str], expected_authentication_method: AuthenticationMethod
    ) -> None:
        assert get_authentication_method(provider, authentication) is expected_authentication_method