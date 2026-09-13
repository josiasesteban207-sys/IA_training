import torch.nn as nn


class IrisNetwork(nn.Module):

    def __init__(self):

        super().__init__()

        self.red = nn.Sequential(

            nn.Linear(

                4,

                16

            ),

            nn.ReLU(),

            nn.Linear(

                16,

                8

            ),

            nn.ReLU(),

            nn.Linear(

                8,

                3

            )

        )

    def forward(

        self,

        x

    ):

        return self.red(

            x

        )