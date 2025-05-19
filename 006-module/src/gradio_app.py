import gradio as gr
from agents.trend_confirmation import get_trend_confirmation
from agents.momentum_signal import get_momentum_signal
from agents.volume_confirmation import get_volume_confirmation
from agents.support_resistance import get_support_resistance

class GradioStockAnalyzer:
    def __init__(self, engines, llm_client):
        self.engines = engines
        self.llm_client = llm_client

    def get_company_details(self, symbol):
        try:
            results = self.engines['generic'].search(symbol, top_k=1)
            if results:
                stock = results[0]
                details = f"""
Symbol: {stock.metadata.get('symbol', '')}
Name: {stock.metadata.get('name', '')}
Sector: {stock.metadata.get('sector', '')}
Industry: {stock.metadata.get('industry', '')}
Market Cap: {stock.metadata.get('market_cap', '')}
"""
                return details
            else:
                return "No company details found."
        except Exception as e:
            return f"Error: {str(e)}"

    def get_qdrant_details(self, symbol):
        try:
            if 'qdrant' not in self.engines:
                return "Qdrant engine is not available. Please check initialization."
            results = self.engines['qdrant'].search(symbol, top_k=1)
            if results:
                stock = results[0]
                details = f"""
Symbol: {stock.metadata.get('symbol', '')}
Name: {stock.metadata.get('name', '')}
Sector: {stock.metadata.get('sector', '')}
Industry: {stock.metadata.get('industry', '')}
Market Cap: {stock.metadata.get('market_cap', '')}
"""
                return details
            else:
                return "No Qdrant details found."
        except Exception as e:
            return f"Qdrant Error: {str(e)}"

    def get_duckduckgo_details(self, symbol):
        try:
            results = self.engines['duckduckgo'].search(symbol, top_k=1)
            if results:
                stock = results[0]
                details = f"""
Title: {stock.title}
URL: {stock.url}
Snippet: {stock.snippet}
"""
                return details
            else:
                return "No DuckDuckGo details found."
        except Exception as e:
            return f"Error: {str(e)}"

    def get_llm_prediction(self, symbol):
        try:
            # Collect indicator results
            trend = get_trend_confirmation(symbol)
            momentum = get_momentum_signal(symbol)
            volume = get_volume_confirmation(symbol)
            support_res = get_support_resistance(symbol)

            # Optionally, still get the generic stock search result
            results = self.engines['generic'].search(symbol, top_k=1)
            stock = results[0] if results else None

            context = {
                "query": symbol,
                "engine": "generic",
                "stock": {
                    "title": stock.title if stock else None,
                    "score": stock.score if stock else None,
                    "url": stock.url if stock else None,
                    "snippet": stock.snippet if stock else None,
                    "metadata": stock.metadata if stock else None,
                    "raw_response": stock.raw_response if stock else None
                } if stock else None,
                "indicators": {
                    "trend_confirmation": trend,
                    "momentum_signal": momentum,
                    "volume_confirmation": volume,
                    "support_resistance": support_res
                }
            }

            prompt = (
                "You are a stock trading assistant. You are given the following technical indicators for a stock symbol: "
                "Trend Confirmation, Momentum Signal (RSI or MACD), Volume Confirmation, and Support/Resistance Levels. "
                "For each indicator, provide a brief analysis of what it reveals about the stock's current situation. "
                "Explain what each indicator is showing and how it contributes to the overall assessment. "
                "Then, based on the combined insights, output a single word: BUY, SELL, or NEUTRAL, and provide a concise reasoning using the indicators.\n"
                "\n"
                "- Trend Confirmation: Indicates the overall direction of the price movement (uptrend, downtrend, or sideways/uncertain). An uptrend suggests bullish sentiment, a downtrend suggests bearish sentiment.\n"
                "- Momentum Signal: Measures the strength and speed of the price movement. RSI > 70 is overbought (potential reversal or sell), RSI < 30 is oversold (potential reversal or buy), MACD crossovers indicate momentum shifts.\n"
                "- Volume Confirmation: Assesses whether trading volume supports the price move. Rising volume with price increases confirms bullish moves; rising volume with price decreases confirms bearish moves. Low or diverging volume may signal weak trends.\n"
                "- Support/Resistance: Identifies key price levels where the stock tends to reverse or pause. Price near support may bounce (buy opportunity), price near resistance may fall (sell opportunity).\n"
                "\n"
                "For each indicator, explain what it is currently signaling for the given stock symbol. Then, synthesize the information and provide a clear, actionable recommendation (BUY, SELL, or NEUTRAL) with a concise justification."
            )

            llm_response = self.llm_client.generate(
                prompt=prompt,
                context=context
            )
            return llm_response
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_stock(self, symbol):
        company = self.get_company_details(symbol)
        qdrant = self.get_qdrant_details(symbol)
        duck = self.get_duckduckgo_details(symbol)
        llm = self.get_llm_prediction(symbol)
        # Ensure all are strings and not None
        company = str(company) if company is not None else ""
        qdrant = str(qdrant) if qdrant is not None else ""
        duck = str(duck) if duck is not None else ""
        llm = str(llm) if llm is not None else ""
        return company, qdrant, duck, llm

    def launch(self):
        def gradio_fn(symbol):
            result = self.analyze_stock(symbol)
            # Ensure result is a tuple of four strings
            if not isinstance(result, tuple) or len(result) != 4:
                return ("", "", "", "")
            return tuple(str(x) if x is not None else "" for x in result)
        with gr.Blocks() as demo:
            gr.Markdown("## Stock Symbol Analysis")
            symbol_input = gr.Textbox(label="Stock Symbol to analyse")
            analyze_btn = gr.Button("Analyze")
            with gr.Row():
                with gr.Column(scale=1):
                    company_box = gr.Textbox(label="Company Details from Generic Search", lines=8)
                    qdrant_box = gr.Textbox(label="Qdrant Search Output", lines=8)
                    duck_box = gr.Textbox(label="DuckDuckGo Search Output", lines=8)
                with gr.Column(scale=2):
                    llm_box = gr.Textbox(label="Buy/Sell Prediction Result", lines=10)
            analyze_btn.click(gradio_fn, inputs=symbol_input, outputs=[company_box, qdrant_box, duck_box, llm_box])
        demo.launch()

def launch_gradio_app(engines, llm_client):
    analyzer = GradioStockAnalyzer(engines, llm_client)
    analyzer.launch() 