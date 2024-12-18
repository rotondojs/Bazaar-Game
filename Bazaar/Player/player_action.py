from enum import StrEnum, auto
from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional


class ActionType(StrEnum):
    """
    Enumeration of possible action types in the game that can be made by the player.
    """

    GET_PEBBLE = auto()
    USE_EQUATION = auto()
    PURCHASE_CARD = auto()


class _PlayerActionOptions(BaseModel):
    """
    Represents the options for a player's action.

    Attributes:
        action_type (ActionType): The type of action being performed.
        index (Optional[int]): The index associated with the action, if applicable.
        right_to_left (Optional[bool]): The direction of the action, if applicable.
    """

    action_type: ActionType
    index: Optional[int] = None
    right_to_left: Optional[bool] = None

    def __init__(self, action_type: ActionType, index: Optional[int] = None, right_to_left: Optional[bool] = None):
        super().__init__(action_type=action_type, index=index, right_to_left=right_to_left)

    @model_validator(mode="after")
    def validate_options(self) -> "_PlayerActionOptions":
        """
        Validates the options for a player action based on the action type.

        Raises:
            ValueError: If the options are invalid for the given action type.
        """
        validation_methods = {
            ActionType.USE_EQUATION: self._validate_use_equation,
            ActionType.PURCHASE_CARD: self._validate_purchase_card,
            ActionType.GET_PEBBLE: self._validate_no_options
        }

        validation_method = validation_methods.get(self.action_type)

        if validation_method:
            validation_method()
        else:
            raise ValueError(f"Invalid action type: {self.action_type}")

        return self

    def __eq__(self, other: "_PlayerActionOptions") -> bool:
        return (
            self.action_type == other.action_type
            and self.index == other.index
            and self.right_to_left == other.right_to_left
        )

    def __hash__(self) -> int:
        return hash((self.action_type, self.index, self.right_to_left))

    def _validate_use_equation(self) -> None:
        if self.index is None:
            raise ValueError("'index' must be defined for USE_EQUATION action.")
        if self.right_to_left is None:
            raise ValueError(
                "Both 'right_to_left' and 'index' must be defined for USE_EQUATION action."
            )

    def _validate_purchase_card(self) -> None:
        if self.index is None:
            raise ValueError("'index' must be defined for PURCHASE_CARD action.")
        if self.right_to_left is not None:
            raise ValueError(
                "'right_to_left' should not be defined for PURCHASE_CARD action."
            )

    def _validate_no_options(self) -> None:
        if self.index is not None or self.right_to_left is not None:
            raise ValueError(
                f"No options should be defined for {self.action_type} action."
            )


class PlayerAction(BaseModel):
    """
    Represents a player's action in the game.

    Attributes:
        action_type (ActionType): The type of action being performed.
        options (PlayerActionOptions): The options associated with the action.
    """

    action_type: ActionType
    options: Annotated[
        _PlayerActionOptions, Field(default_factory=_PlayerActionOptions)
    ]

    def __init__(self, action_type: ActionType, **options):
        """
        Initializes a new PlayerAction instance.

        Arguments:
            action (ActionType): The type of action being performed.
            **options: Additional keyword arguments for the action options.
        """
        super().__init__(
            action_type=action_type,
            options=_PlayerActionOptions(action_type=action_type, **options),
        )

    def __repr__(self) -> str:
        options = ", ".join(
            f"{key}={value!r}"
            for key, value in self.options.__dict__.items()
            if key != "action_type"
        )
        return f"{self.__class__.__name__}(action: {self.action_type}, {options})"

    def __eq__(self, other: "PlayerAction") -> bool:
        return (
            self.action_type == other.action_type
            and self.options == other.options
        )

    def __hash__(self) -> int:
        return hash((self.action_type, self.options))
