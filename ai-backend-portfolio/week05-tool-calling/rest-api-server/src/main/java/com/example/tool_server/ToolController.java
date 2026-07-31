package com.example.tool_server;

import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
public class ToolController {

    @GetMapping("/weather/{city}")
    public Map<String, Object> getWeather(@PathVariable String city) {
        return Map.of(
            "city", city,
            "temperature_celsius", 32,
            "condition", "Humid and partly cloudy",
            "humidity_percent", 78
        );
    }

    @GetMapping("/currency/convert")
    public Map<String, Object> convertCurrency(
            @RequestParam double amount,
            @RequestParam String from,
            @RequestParam String to) {
        double rate = getRate(from, to);
        return Map.of(
            "from", from,
            "to", to,
            "amount", amount,
            "converted", Math.round(amount * rate * 100.0) / 100.0,
            "rate", rate
        );
    }

    private double getRate(String from, String to) {
        String pair = from.toUpperCase() + "_" + to.toUpperCase();
        return switch (pair) {
            case "USD_BDT" -> 110.5;
            case "BDT_USD" -> 0.009;
            case "USD_EUR" -> 0.92;
            case "EUR_USD" -> 1.09;
            default -> 1.0;
        };
    }
}