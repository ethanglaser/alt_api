import Layout from "layouts/main";
import { FunctionComponent } from "react";
import { Heading, Flex, Container, Button } from "@chakra-ui/react";
import SEO from "components/SEO";

const Index: FunctionComponent = () => {
  return (
    <Layout>
      <SEO page="home" />

      <Container py={20} maxW="container.xl">
        <Flex mb={10} width="full" align="center" justifyContent="center">
          <Heading as="h2">Home</Heading>
        </Flex>
        <Button mt="6" onClick={() => {
          alert('hi')
        }}>Hello world</Button>
      </Container>
    </Layout>
  );
};

export default Index;
