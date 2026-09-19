package com.example.consumer;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;

@Component
public class EventListener {

    @Value("${ai.service.url}")
    private String aiServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper mapper = new ObjectMapper();

    @KafkaListener(topics = "business-events", groupId = "ai-enrichment-group")
    public void consume(String message) {
        try {
            Map<String, Object> event = mapper.readValue(message, Map.class);
            System.out.println("Received event: " + event.get("event_id"));

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(message, headers);

            ResponseEntity<String> response = restTemplate.postForEntity(
                    aiServiceUrl + "/enrich", request, String.class
            );
            System.out.println("Enriched: " + response.getBody());

        } catch (Exception e) {
            System.err.println("Error processing event: " + e.getMessage());
        }
    }
}