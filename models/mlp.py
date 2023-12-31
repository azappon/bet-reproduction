import torch.nn as nn
import torch.nn.functional as F
import logging

logger = logging.getLogger(__name__)


def mlp(
    input_dim,
    hidden_dim,
    output_dim,
    hidden_depth,
    output_mod=None,
    batchnorm=False,
    activation=nn.ReLU,
):
    """Builds a multi-layer perceptron (MLP) with the specified dimensions.
    Args:
        input_dim (int): Input dimension.
        hidden_dim (int): Hidden dimension.
        output_dim (int): Output dimension.
        hidden_depth (int): Number of hidden layers.
        output_mod (nn.Module): Module to apply to the output of the MLP.
        batchnorm (bool): Whether to use batch normalization.
        activation (nn.Module): Activation function to use.
    Returns:
        nn.Module: MLP.
    """
    # It needs to flatten the observations (but keep the batch size dimension, 0, as is)
    mods = [nn.Flatten(1, -1)]

    # 1st layer
    if hidden_depth == 0:
        mods += [nn.Linear(input_dim, output_dim)]
    else:
        mods += (
            [
                nn.Linear(input_dim, hidden_dim),
                activation(inplace=True),
            ]
            if not batchnorm
            else [
                nn.Linear(input_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                activation(inplace=True),
            ]
        )
        # Hidden layers
        for _ in range(hidden_depth - 1):
            mods += (
                [
                    nn.Linear(hidden_dim, hidden_dim),
                    activation(inplace=True),
                ]
                if not batchnorm
                else [
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.BatchNorm1d(hidden_dim),
                    activation(inplace=True),
                ]
            )
        # Final layer
        mods.append(nn.Linear(hidden_dim, output_dim))
    if output_mod is not None:
        mods.append(output_mod)

    trunk = nn.Sequential(*mods)
    print("MLP Architecture: \n", trunk)

    return trunk


def weight_init(m):
    """Custom weight init for Conv2D and Linear layers.
    Args:
        m (nn.Module): Module to initialize.
    """
    if isinstance(m, nn.Linear):
        nn.init.orthogonal_(m.weight.data)
        if hasattr(m.bias, "data"):
            m.bias.data.fill_(0.0)


class MLP(nn.Module):
    """Multi-layer perceptron (MLP) with the specified dimensions.
    Args:
        input_dim (int): Input dimension.
        hidden_dim (int): Hidden dimension.
        output_dim (int): Output dimension.
        hidden_depth (int): Number of hidden layers.
        output_mod (nn.Module): Module to apply to the output of the MLP.
        batchnorm (bool): Whether to use batch normalization.
        activation (nn.Module): Activation function to use.
    """
    def __init__(
        self,
        input_dim,
        hidden_dim,
        output_dim,
        hidden_depth,
        output_mod=None,
        batchnorm=False,
        activation=nn.ReLU,
    ):
        super().__init__()
        self.trunk = mlp(
            input_dim,
            hidden_dim,
            output_dim,
            hidden_depth,
            output_mod,
            batchnorm=batchnorm,
            activation=activation,
        )
        self.apply(weight_init)

        logger.info(
            "number of parameters: %e", sum(p.numel() for p in self.trunk.parameters())
        )

    def forward(self, x):
        return self.trunk(x)
