import json

from langchain.tools import BaseTool
from solders.pubkey import Pubkey  # type: ignore

from sprout.agent import SolanaAgentKit
from sprout.tools import create_image
from sprout.utils import toJSON
from sprout.utils.meteora_dlmm.types import ActivationType


class SolanaBalanceTool(BaseTool):
    name:str = "solana_balance"
    description:str = """
    Get the balance of a Solana wallet or token account.

    If you want to get the balance of your wallet, you don't need to provide the tokenAddress.
    If no tokenAddress is provided, the balance will be in SOL.
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            token_address = Pubkey.from_string(input) if input else None
            balance = await self.solana_kit.get_balance(token_address)
            return {
                "status": "success",
                "balance": balance,
                "token": input or "SOL",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTransferTool(BaseTool):
    name:str = "solana_transfer"
    description:str = """
    Transfer tokens or SOL to another address.

    Input (JSON string):
    {
        "to": "wallet_address",
        "amount": 1,
        "mint": "mint_address" (optional)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            recipient = Pubkey.from_string(data["to"])
            mint_address = Pubkey.from_string(data["mint"]) if "mint" in data else None

            transaction = await self.solana_kit.transfer(recipient, data["amount"], mint_address)

            return {
                "status": "success",
                "message": "Transfer completed successfully",
                "amount": data["amount"],
                "recipient": data["to"],
                "token": data.get("mint", "SOL"),
                "transaction": transaction,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaDeployTokenTool(BaseTool):
    name:str = "solana_deploy_token"
    description:str = """
    Deploy a new SPL token. Input should be JSON string with:
    {
        "decimals": 9,
        "initialSupply": 1000
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            decimals = data.get("decimals", 9)

            if decimals < 0 or decimals > 9:
                raise ValueError("Decimals must be between 0 and 9")

            token_details = await self.solana_kit.deploy_token(decimals)
            return {
                "status": "success",
                "message": "Token deployed successfully",
                "mintAddress": token_details["mint"],
                "decimals": decimals,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaTradeTool(BaseTool):
    name:str = "solana_trade"
    description:str = """
    Execute a trade on Solana.

    Input (JSON string):
    {
        "output_mint": "output_mint_address",
        "input_amount": 100,
        "input_mint": "input_mint_address" (optional),
        "slippage_bps": 100 (optional)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            output_mint = Pubkey.from_string(data["output_mint"])
            input_mint = Pubkey.from_string(data["input_mint"]) if "input_mint" in data else None
            slippage_bps = data.get("slippage_bps", 100)

            transaction = await self.solana_kit.trade(
                output_mint, data["input_amount"], input_mint, slippage_bps
            )

            return {
                "status": "success",
                "message": "Trade executed successfully",
                "transaction": transaction,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaFaucetTool(BaseTool):
    name:str = "solana_request_funds"
    description:str = "Request test funds from a Solana faucet."
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            result = await self.solana_kit.request_faucet_funds()
            return {
                "status": "success",
                "message": "Faucet funds requested successfully",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaStakeTool(BaseTool):
    name:str = "solana_stake"
    description:str = "Stake assets on Solana. Input is the amount to stake."
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            amount = int(input)
            result = await self.solana_kit.stake(amount)
            return {
                "status": "success",
                "message": "Assets staked successfully",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetWalletAddressTool(BaseTool):
    name:str = "solana_get_wallet_address"
    description:str = "Get the wallet address of the agent"
    solana_kit: SolanaAgentKit
    
    async def _arun(self):
        try:
            result = await self.solana_kit.wallet_address
            return {
                "status": "success",
                "message": "Wallet address fetched successfully",
                "result": str(result),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaCreateImageTool(BaseTool):
    name: str = "solana_create_image"
    description: str = """
    Create an image using OpenAI's DALL-E.

    Input (JSON string):
    {
        "prompt": "description of the image",
        "size": "image_size" (optional, default: "1024x1024"),
        "n": "number_of_images" (optional, default: 1)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            prompt = data["prompt"]
            size = data.get("size", "1024x1024")
            n = data.get("n", 1)

            if not prompt.strip():
                raise ValueError("Prompt must be a non-empty string.")

            result = await create_image(self.solana_kit, prompt, size, n)

            return {
                "status": "success",
                "message": "Image created successfully",
                "images": result["images"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR")
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTPSCalculatorTool(BaseTool):
    name: str = "solana_get_tps"
    description: str = "Get the current TPS of the Solana network."
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            tps = await self.solana_kit.get_tps()

            return {
                "status": "success",
                "message": f"Solana (mainnet-beta) current transactions per second: {tps}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error fetching TPS: {str(e)}",
                "code": getattr(e, "code", "UNKNOWN_ERROR")
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaPumpFunTokenTool(BaseTool):
    name:str = "solana_launch_pump_fun_token"
    description:str = """
    Launch a Pump Fun token on Solana.

    Input (JSON string):
    {
        "token_name": "MyToken",
        "token_ticker": "MTK",
        "description": "A test token",
        "image_url": "http://example.com/image.png"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            result = await self.solana_kit.launch_pump_fun_token(
                data["token_name"],
                data["token_ticker"],
                data["description"],
                data["image_url"],
                options=data.get("options")
            )
            return {
                "status": "success",
                "message": "Pump Fun token launched successfully",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaFetchPriceTool(BaseTool):
    """
    Tool to fetch the price of a token in USDC.
    """
    name:str = "solana_fetch_price"
    description:str = """Fetch the price of a given token in USDC.

    Inputs:
    - tokenId: string, the mint address of the token, e.g., "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
    """
    solana_kit: SolanaAgentKit

    async def call(self, input: str) -> str:
        try:
            token_id = input.strip()
            price = await self.solana_kit.fetch_price(token_id)
            return json.dumps({
                "status": "success",
                "tokenId": token_id,
                "priceInUSDC": price,
            })
        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "UNKNOWN_ERROR"),
            })
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTokenDataTool(BaseTool):
    """
    Tool to fetch token data for a given token mint address.
    """
    name:str = "solana_token_data"
    description:str = """Get the token data for a given token mint address.

    Inputs:
    - mintAddress: string, e.g., "So11111111111111111111111111111111111111112" (required)
    """
    solana_kit: SolanaAgentKit

    async def call(self, input: str) -> str:
        try:
            mint_address = input.strip()
            token_data = await self.solana_kit.get_token_data_by_address(mint_address)
            return json.dumps({
                "status": "success",
                "tokenData": token_data,
            })
        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "UNKNOWN_ERROR"),
            })
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaTokenDataByTickerTool(BaseTool):
    """
    Tool to fetch token data for a given token ticker.
    """
    name:str = "solana_token_data_by_ticker"
    description:str = """Get the token data for a given token ticker.

    Inputs:
    - ticker: string, e.g., "USDC" (required)
    """
    solana_kit: SolanaAgentKit

    async def call(self, input: str) -> str:
        try:
            ticker = input.strip()
            token_data = await self.solana_kit.get_token_data_by_ticker(ticker)
            return json.dumps({
                "status": "success",
                "tokenData": token_data,
            })
        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "UNKNOWN_ERROR"),
            })
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaMeteoraDLMMTool(BaseTool):
    """
    Tool to create dlmm pool on meteora.
    """
    name: str = "solana_create_meteora_dlmm_pool"
    description: str = """
    Create a Meteora DLMM Pool on Solana.

    Input (JSON string):
    {
        "bin_step": 5,
        "token_a_mint": "7S3d7xxFPgFhVde8XwDoQG9N7kF8Vo48ghAhoNxd34Zp",
        "token_b_mint": "A1b1xxFPgFhVde8XwDoQG9N7kF8Vo48ghAhoNxd34Zp",
        "initial_price": 1.23,
        "price_rounding_up": true,
        "fee_bps": 300,
        "activation_type": "Instant",  // Options: "Instant", "Delayed", "Manual"
        "has_alpha_vault": false,
        "activation_point": null      // Optional, only for Delayed type
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str) -> dict:
        try:
            # Parse input
            data = toJSON(input)

            # Ensure required keys exist
            required_keys = [
                "bin_step",
                "token_a_mint",
                "token_b_mint",
                "initial_price",
                "price_rounding_up",
                "fee_bps",
                "activation_type",
                "has_alpha_vault"
            ]
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required key: {key}")

            activation_type_mapping = {
                "Slot": ActivationType.Slot,
                "Timestamp": ActivationType.Timestamp,
            }
            activation_type = activation_type_mapping.get(data["activation_type"])
            if activation_type is None:
                raise ValueError("Invalid activation_type. Valid options are: Slot, Timestamp.")

            activation_point = data.get("activation_point", None)

            result = await self.solana_kit.create_meteora_dlmm_pool(
                bin_step=data["bin_step"],
                token_a_mint=data["token_a_mint"],
                token_b_mint=data["token_b_mint"],
                initial_price=data["initial_price"],
                price_rounding_up=data["price_rounding_up"],
                fee_bps=data["fee_bps"],
                activation_type=activation_type,
                has_alpha_vault=data["has_alpha_vault"],
                activation_point=activation_point
            )

            return {
                "status": "success",
                "message": "Meteora DLMM pool created successfully",
                "result": result,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to process input: {input}. Error: {str(e)}",
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaRaydiumBuyTool(BaseTool):
    name: str = "raydium_buy"
    description: str = """
    Buy tokens using Raydium's swap functionality.

    Input (JSON string):
    {
        "pair_address": "address_of_the_trading_pair",
        "sol_in": 0.01,  # Amount of SOL to spend (optional, defaults to 0.01)
        "slippage": 5  # Slippage tolerance in percentage (optional, defaults to 5)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            pair_address = data["pair_address"]
            sol_in = data.get("sol_in", 0.01)  # Default to 0.01 SOL if not provided
            slippage = data.get("slippage", 5)  # Default to 5% slippage if not provided

            result = await self.solana_kit.buy_with_raydium(pair_address, sol_in, slippage)

            return {
                "status": "success",
                "message": "Buy transaction completed successfully",
                "pair_address": pair_address,
                "sol_in": sol_in,
                "slippage": slippage,
                "transaction": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaRaydiumSellTool(BaseTool):
    name: str = "raydium_sell"
    description: str = """
    Sell tokens using Raydium's swap functionality.

    Input (JSON string):
    {
        "pair_address": "address_of_the_trading_pair",
        "percentage": 100,  # Percentage of tokens to sell (optional, defaults to 100)
        "slippage": 5  # Slippage tolerance in percentage (optional, defaults to 5)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            pair_address = data["pair_address"]
            percentage = data.get("percentage", 100)  # Default to 100% if not provided
            slippage = data.get("slippage", 5)  # Default to 5% slippage if not provided

            result = await self.solana_kit.sell_with_raydium(pair_address, percentage, slippage)

            return {
                "status": "success",
                "message": "Sell transaction completed successfully",
                "pair_address": pair_address,
                "percentage": percentage,
                "slippage": slippage,
                "transaction": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaBurnAndCloseTool(BaseTool):
    name: str = "solana_burn_and_close_account"
    description: str = """
    Burn and close a single Solana token account.

    Input: A JSON string with:
    {
        "token_account": "public_key_of_the_token_account"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            token_account = data["token_account"]

            if not token_account:
                raise ValueError("Token account is required.")

            result = await self.solana_kit.burn_and_close_accounts(token_account)

            return {
                "status": "success",
                "message": "Token account burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaBurnAndCloseMultipleTool(BaseTool):
    name: str = "solana_burn_and_close_multiple_accounts"
    description: str = """
    Burn and close multiple Solana token accounts.

    Input: A JSON string with:
    {
        "token_accounts": ["public_key_1", "public_key_2", ...]
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            token_accounts = data.get("token_accounts", [])

            if not isinstance(token_accounts, list) or not token_accounts:
                raise ValueError("A list of token accounts is required.")

            result = await self.solana_kit.multiple_burn_and_close_accounts(token_accounts)

            return {
                "status": "success",
                "message": "Token accounts burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaCreateGibworkTaskTool(BaseTool):
    name: str = "solana_create_gibwork_task"
    description: str = """
    Create an new task on Gibwork

    Input: A JSON string with:
    {
        "title": "title of the task",
        "content: "description of the task",
        "requirements": "requirements to complete the task",
        "tags": ["tag1", "tag2", ...] # list of tags associated with the task,
        "token_mint_address": "token mint address for payment",
        "token_amount": 1000 # amount of token to pay for the task
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            title = data["title"]
            content = data["content"]
            requirements = data["requirements"]
            tags = data.get("tags", [])
            token_mint_address = Pubkey.from_string(data["token_mint_address"])
            token_amount = data["token_amount"]
            
            result = await self.solana_kit.create_gibwork_task(title, content, requirements, tags, token_mint_address, token_amount)

            return {
                "status": "success",
                "message": "Token accounts burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }


    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaCreateGibworkTaskTool(BaseTool):
    name: str = "solana_create_gibwork_task"
    description: str = """
    Create an new task on Gibwork

    Input: A JSON string with:
    {
        "title": "title of the task",
        "content: "description of the task",
        "requirements": "requirements to complete the task",
        "tags": ["tag1", "tag2", ...] # list of tags associated with the task,
        "token_mint_address": "token mint address for payment",
        "token_amount": 1000 # amount of token to pay for the task
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            title = data["title"]
            content = data["content"]
            requirements = data["requirements"]
            tags = data.get("tags", [])
            token_mint_address = Pubkey.from_string(data["token_mint_address"])
            token_amount = data["token_amount"]
            
            result = await self.solana_kit.create_gibwork_task(title, content, requirements, tags, token_mint_address, token_amount)

            return {
                "status": "success",
                "message": "Token accounts burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaBuyUsingMoonshotTool(BaseTool):
    name: str = "solana_buy_using_moonshot"
    description:str = """
    Buy a token using Moonshot.

    Input: A JSON string with:
    {
        "mint_str": "string, the mint address of the token to buy",
        "collateral_amount": 0.01, # optional, collateral amount in SOL to use for the purchase (default: 0.01)
        "slippage_bps": 500 # optional, slippage in basis points (default: 500)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            mint_str = data["mint_str"]
            collateral_amount = data.get("collateral_amount", 0.01)
            slippage_bps = data.get("slippage_bps", 500)
            
            result = await self.solana_kit.buy_using_moonshot(mint_str, collateral_amount, slippage_bps)

            return {
                "status": "success",
                "message": "Token purchased successfully using Moonshot.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaSellUsingMoonshotTool(BaseTool):
    name: str = "solana_sell_using_moonshot"
    description:str = """
    Sell a token using Moonshot.

    Input: A JSON string with:
    {
        "mint_str": "string, the mint address of the token to sell",
        "token_balance": 0.01, # optional, token balance to sell (default: 0.01)
        "slippage_bps": 500 # optional, slippage in basis points (default: 500)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = toJSON(input)
            mint_str = data["mint_str"]
            token_balance = data.get("token_balance", 0.01)
            slippage_bps = data.get("slippage_bps", 500)
            
            result = await self.solana_kit.sell_using_moonshot(mint_str, token_balance, slippage_bps)

            return {
                "status": "success",
                "message": "Token sold successfully using Moonshot.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
            
class SolanaPythGetPriceTool(BaseTool):
    name: str = "solana_pyth_get_price"
    description: str = """
    Fetch the price of a token using the Pyth Oracle.

    Input: A JSON string with:
    {
        "mint_address": "string, the mint address of the token"
    }

    Output:
    {
        "price": float, # the token price (if trading),
        "confidence_interval": float, # the confidence interval (if trading),
        "status": "UNKNOWN", "TRADING", "HALTED", "AUCTION", "IGNORED",
        "message": "string, if not trading"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            mint_address = data["mint_address"]

            result = await self.solana_kit.pythFetchPrice(mint_address)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

def create_solana_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaBalanceTool(solana_kit=solana_kit),
        SolanaTransferTool(solana_kit=solana_kit),
        SolanaDeployTokenTool(solana_kit=solana_kit),
        SolanaTradeTool(solana_kit=solana_kit),
        SolanaFaucetTool(solana_kit=solana_kit),
        SolanaStakeTool(solana_kit=solana_kit),
        SolanaPumpFunTokenTool(solana_kit=solana_kit),
        SolanaCreateImageTool(solana_kit=solana_kit),
        SolanaGetWalletAddressTool(solana_kit=solana_kit),
        SolanaTPSCalculatorTool(solana_kit=solana_kit),
        SolanaFetchPriceTool(solana_kit=solana_kit),
        SolanaTokenDataTool(solana_kit=solana_kit),
        SolanaTokenDataByTickerTool(solana_kit=solana_kit),
        SolanaMeteoraDLMMTool(solana_kit=solana_kit),
        SolanaRaydiumBuyTool(solana_kit=solana_kit),
        SolanaRaydiumSellTool(solana_kit=solana_kit),
        SolanaCreateGibworkTaskTool(solana_kit=solana_kit),
        SolanaSellUsingMoonshotTool(solana_kit=solana_kit),
        SolanaBuyUsingMoonshotTool(solana_kit=solana_kit),
        SolanaPythGetPriceTool(solana_kit=solana_kit)
    ]

