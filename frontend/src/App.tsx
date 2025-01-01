import React, { useEffect, useState } from 'react';
import { ChakraProvider, Box, Container, Heading, SimpleGrid, Text, Select } from '@chakra-ui/react';
import axios from 'axios';

interface NewsArticle {
  title: string;
  description: string;
  url: string;
  source: string;
  category: string;
}

function App() {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [category, setCategory] = useState<string>('');
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await axios.get(`${apiUrl}/api/news${category ? `?category=${category}` : ''}`);
        setArticles(response.data);
      } catch (error) {
        console.error('Error fetching news:', error);
      }
    };

    fetchNews();
  }, [category]);

  return (
    <ChakraProvider>
      <Box bg="gray.50" minH="100vh" py={8}>
        <Container maxW="container.xl">
          <Heading mb={8} textAlign="center">Smart News</Heading>
          
          <Select
            placeholder="Select category"
            mb={8}
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="business">Business</option>
            <option value="technology">Technology</option>
            <option value="science">Science</option>
            <option value="health">Health</option>
            <option value="entertainment">Entertainment</option>
            <option value="sports">Sports</option>
          </Select>

          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8}>
            {articles.map((article, index) => (
              <Box
                key={index}
                bg="white"
                p={6}
                rounded="lg"
                shadow="md"
                _hover={{ transform: 'translateY(-2px)', shadow: 'lg' }}
                transition="all 0.2s"
              >
                <Heading size="md" mb={2}>
                  <a href={article.url} target="_blank" rel="noopener noreferrer">
                    {article.title}
                  </a>
                </Heading>
                <Text color="gray.600">{article.description}</Text>
                <Text mt={4} color="gray.500" fontSize="sm">
                  Source: {article.source}
                </Text>
              </Box>
            ))}
          </SimpleGrid>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
