from grid.commands.commands import addsibling_cmd
from grid.commands.commands import updatenet_cmd
from grid.commands.commands import syncgrid_cmd
from grid.commands.commands import updateenergy_cmd

commands = {
    'UpdateEnergy': updateenergy_cmd,
    'UpdateNet': updatenet_cmd,
    'SyncGrid': syncgrid_cmd,
    'AddSibling': addsibling_cmd
}


__all__ = ['commands']
